"""Sequential and parallel animation composition."""
from __future__ import annotations

import time
from collections.abc import Iterable

from ..core.animation import Animation
from ..core.scheduler import scheduler_for


class _Group:
    def __init__(self, animations: Iterable[Animation]) -> None:
        self.animations = list(animations)
        if not self.animations:
            raise ValueError("an animation group cannot be empty")
        self.widget = self.animations[0].widget
        root = self.widget.winfo_toplevel()
        if any(animation.widget.winfo_toplevel() is not root for animation in self.animations):
            raise ValueError("grouped animations must share one Tk interpreter")
        self.scheduler = scheduler_for(self.widget)
        self.state = "idle"
        self._started = 0.0
        self._paused = 0.0
        self._paused_animations: set[Animation] = set()
        self.on_complete = None

    def pause(self):
        if self.state == "running":
            self.state, self._paused = "paused", time.monotonic()
            self.scheduler.remove(self._tick)
            candidates = self.animations[self._index:] if isinstance(self, Sequence) else self.animations
            self._paused_animations = {animation for animation in candidates if animation.state == "running"}
            for animation in self._paused_animations:
                animation.pause()
        return self

    def resume(self):
        if self.state == "paused":
            self._started += time.monotonic() - self._paused
            self.state = "running"
            for animation in self._paused_animations:
                animation.resume()
            self._paused_animations.clear()
            self.scheduler.add(self._tick)
        return self
    def cancel(self):
        if self.state in ("running", "paused"):
            self.scheduler.remove(self._tick)
            for animation in self.animations:
                if animation.state in ("running", "paused"):
                    animation.cancel()
            self.state = "cancelled"
        return self

    def reset(self):
        self.scheduler.remove(self._tick)
        for animation in self.animations:
            animation.reset()
        self.state = "idle"
        self._paused_animations.clear()
        return self

    def restart(self):
        return self.reset().start()

    def _complete(self) -> None:
        self.state = "completed"
        if self.on_complete:
            self.on_complete()

class Sequence(_Group):
    """Play animations one after another."""
    def __init__(self, animations: Iterable[Animation]) -> None:
        super().__init__(animations)
        self._index = 0

    def start(self):
        self.reset()
        self.state, self._started = "running", time.monotonic()
        self._index = 0
        self.animations[0].start()
        self.scheduler.add(self._tick)
        return self

    def _tick(self, now: float):
        if self.state != "running":
            return False
        current = self.animations[self._index]
        if current.state in ("completed", "cancelled"):
            self._index += 1
            if self._index == len(self.animations):
                self._complete()
                return False
            self.animations[self._index].start()
        return True

class Parallel(_Group):
    """Play animations at the same time."""
    def start(self):
        self.reset()
        self.state, self._started = "running", time.monotonic()
        for animation in self.animations:
            animation.start()
        self.scheduler.add(self._tick)
        return self

    def _tick(self, now: float):
        if self.state != "running":
            return False
        if all(a.state in ("completed", "cancelled") for a in self.animations):
            self._complete()
            return False
        return True


def stagger(animations: Iterable[Animation], delay_ms: float) -> Sequence:
    """Start each animation in sequence with the given delay between starts."""
    if delay_ms < 0:
        raise ValueError("delay_ms must be non-negative")
    items = list(animations)
    for index, animation in enumerate(items):
        animation.delay += index * delay_ms / 1000
    return Sequence(items)
