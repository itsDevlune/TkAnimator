"""Animation lifecycle and numeric tween primitive."""
from __future__ import annotations

import time
import tkinter as tk
from collections.abc import Callable
from math import isfinite
from typing import Any

from .easing import Easing, EasingFunction, resolve_easing
from .interpolation import interpolate
from .scheduler import Scheduler, scheduler_for


class Animation:
    """A cancellable numeric tween driven by the Tk event loop."""
    def __init__(self, widget: tk.Misc, update: Callable[[float], None], *,
                 duration: float = 1000, delay: float = 0, easing: EasingFunction | Easing = Easing.LINEAR,
                 fps: int = 60, repeat: int = 0, yoyo: bool = False,
                 on_start: Callable[[], None] | None = None,
                 on_update: Callable[[float], None] | None = None,
                 on_complete: Callable[[], None] | None = None,
                 on_cancel: Callable[[], None] | None = None,
                 conflict_key: object | None = None,
                 conflict: str = "replace") -> None:
        if not isfinite(duration) or not isfinite(delay) or duration < 0 or delay < 0:
            raise ValueError("duration and delay must be finite and non-negative")
        if repeat < -1:
            raise ValueError("repeat must be -1 (infinite) or non-negative")
        if not isfinite(fps) or fps < 1:
            raise ValueError("fps must be positive")
        if not callable(update):
            raise TypeError("update must be callable")
        if conflict not in ("replace", "ignore", "allow"):
            raise ValueError("conflict must be 'replace', 'ignore', or 'allow'")
        self.widget, self.update_fn = widget, update
        self.conflict_key, self.conflict_policy = conflict_key, conflict
        self.duration, self.delay = duration / 1000, delay / 1000
        self.easing = resolve_easing(easing)
        self.repeat, self.yoyo = repeat, yoyo
        self._speed = 1.0
        self.on_start, self.on_update = on_start, on_update
        self.on_complete, self.on_cancel = on_complete, on_cancel
        self.scheduler: Scheduler = scheduler_for(widget, max(1, round(1000 / fps)))
        self.state = "idle"
        self.progress = 0.0
        self._started_at = 0.0
        self._cycle_started_at = 0.0
        self._initial_delay = self.delay
        self._paused_at = 0.0
        self._completed_cycles = 0
        self._reverse = False
        self._last_progress: float | None = None
        self._yoyo_final_reverse = False
        self._has_started = False

    @property
    def speed(self) -> float:
        """Playback speed multiplier; 2.0 plays twice as fast."""
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        if not isfinite(value) or value <= 0:
            raise ValueError("speed must be positive")
        if hasattr(self, "_speed") and self.state == "running":
            now = time.monotonic()
            elapsed = max(0.0, (now - self._started_at) * self._speed)
            delay_elapsed = max(0.0, (now - self._cycle_started_at) * self._speed)
            self._started_at = now - elapsed / value
            self._cycle_started_at = now - delay_elapsed / value
        self._speed = float(value)

    def start(self) -> Animation:
        if self.state in ("completed", "cancelled"):
            self.reset()
        if self.state == "running":
            return self
        self.state = "running"
        self._started_at = time.monotonic()
        self._cycle_started_at = self._started_at
        self.delay = self._initial_delay
        self._completed_cycles = 0
        self._reverse = False
        self._yoyo_final_reverse = bool(self.yoyo and self.repeat >= 0 and self.repeat % 2 == 1)
        self.progress = 0.0
        self._last_progress = None
        self._has_started = False
        if self.conflict_key is not None and self.conflict_policy != "allow":
            key = (id(self.widget), self.conflict_key)
            existing = _ACTIVE_CONFLICTS.get(key)
            if existing is not None and existing is not self and existing.state == "running":
                if self.conflict_policy == "ignore":
                    self.state = "cancelled"
                    return self
                existing.cancel()
            _ACTIVE_CONFLICTS[key] = self
        self.scheduler.add(self._tick)
        return self

    def pause(self) -> Animation:
        if self.state == "running":
            self.state = "paused"
            self._paused_at = time.monotonic()
            self.scheduler.remove(self._tick)
        return self

    def resume(self) -> Animation:
        if self.state == "paused":
            shift = (time.monotonic() - self._paused_at) * self.speed
            self._started_at += shift
            self._cycle_started_at += shift
            self.state = "running"
            self.scheduler.add(self._tick)
        return self

    def cancel(self) -> Animation:
        if self.state in ("running", "paused"):
            self.scheduler.remove(self._tick)
            self.state = "cancelled"
            self._release_conflict()
            if self.on_cancel:
                self.on_cancel()
        return self

    def reset(self) -> Animation:
        self.scheduler.remove(self._tick)
        self.state, self.progress = "idle", 0.0
        self._release_conflict()
        self._completed_cycles, self._reverse = 0, False
        self.delay = self._initial_delay
        self._last_progress = None
        self._has_started = False
        self._yoyo_final_reverse = False
        return self

    def restart(self) -> Animation:
        self.reset()
        return self.start()

    def _tick(self, now: float) -> bool:
        if self.state != "running":
            return False
        cycle_elapsed = (now - self._cycle_started_at) * self.speed
        if cycle_elapsed < self.delay:
            return True
        elapsed = (now - self._started_at) * self.speed
        if not self._has_started:
            self._has_started = True
            if self.on_start:
                self.on_start()
        p = 1.0 if self.duration == 0 else min(1.0, elapsed / self.duration)
        if self._reverse:
            p = 1 - p
        eased = self.easing(p)
        self.progress = max(0.0, min(1.0, p))
        self.update_fn(eased)
        if self.on_update:
            self.on_update(self.progress)
        self._last_progress = self.progress
        if elapsed < self.duration:
            return True
        if self.repeat == -1 or self._completed_cycles < self.repeat:
            self._completed_cycles += 1
            if self.yoyo:
                self._reverse = not self._reverse
            if self.duration == 0:
                if self.repeat == -1:
                    self.state = "cancelled"
                    self._release_conflict()
                    if self.on_cancel:
                        self.on_cancel()
                    return False
                self._started_at = now + 1e-6
                self._cycle_started_at = self._started_at
                self.delay = 0
            else:
                self._started_at += (self.duration + self.delay) / self.speed
                self._cycle_started_at = self._started_at
                self.delay = 0
            return True
        if self._yoyo_final_reverse:
            self.progress = 0.0
            self.update_fn(self.easing(0.0))
            if self.on_update:
                self.on_update(0.0)
        self.state = "completed"
        self._release_conflict()
        if self.on_complete:
            self.on_complete()
        return False

    def _release_conflict(self) -> None:
        if self.conflict_key is not None:
            key = (id(self.widget), self.conflict_key)
            if _ACTIVE_CONFLICTS.get(key) is self:
                _ACTIVE_CONFLICTS.pop(key, None)


class Tween(Animation):
    """Animate a numeric value from start to end and call setter on each frame."""
    def __init__(self, widget: tk.Misc, start: float, end: float,
                 setter: Callable[[float], None], **kwargs: Any) -> None:
        self.start_value, self.end_value = start, end
        super().__init__(widget, lambda p: setter(interpolate(start, end, p)), **kwargs)


_ACTIVE_CONFLICTS: dict[tuple[int, object], Animation] = {}
