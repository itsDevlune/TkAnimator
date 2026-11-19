"""A lightweight timeline that schedules animations at offsets."""
from __future__ import annotations

import time
import tkinter as tk

from .animation import Animation
from .scheduler import scheduler_for


class Timeline:
    def __init__(self, widget: tk.Misc) -> None:
        self.widget = widget
        self.scheduler = scheduler_for(widget)
        self._items: list[tuple[float, Animation]] = []
        self.state = "idle"
        self._start = 0.0
        self._paused = 0.0
        self.on_complete = None
        self._paused_animations: set[Animation] = set()

    def add(self, animation: Animation, at_ms: float) -> Timeline:
        if at_ms < 0:
            raise ValueError("timeline offset must be non-negative")
        if animation.widget.winfo_toplevel() is not self.widget.winfo_toplevel():
            raise ValueError("all timeline animations must share the timeline's Tk interpreter")
        self._items.append((at_ms / 1000, animation))
        self._items.sort(key=lambda item: item[0])
        return self

    def start(self):
        self.reset()
        self.state, self._start = "running", time.monotonic()
        if not self._items:
            self.state = "completed"
            if self.on_complete:
                self.on_complete()
            return self
        self.scheduler.add(self._tick)
        return self

    def pause(self):
        if self.state == "running":
            self.state, self._paused = "paused", time.monotonic()
            self.scheduler.remove(self._tick)
            for _, animation in self._items:
                if animation.state == "running":
                    self._paused_animations.add(animation)
                    animation.pause()
        return self

    def resume(self):
        if self.state == "paused":
            self._start += time.monotonic() - self._paused
            self.state = "running"
            for animation in self._paused_animations:
                animation.resume()
            self._paused_animations.clear()
            self.scheduler.add(self._tick)
        return self

    def cancel(self):
        if self.state in ("running", "paused"):
            self.scheduler.remove(self._tick)
            for animation in self._paused_animations:
                animation.resume()
            self._paused_animations.clear()
            for _, animation in self._items:
                if animation.state in ("running", "paused"):
                    animation.cancel()
            self.state = "cancelled"
        return self

    def reset(self):
        self.scheduler.remove(self._tick)
        for _, animation in self._items:
            animation.reset()
        self._paused_animations.clear()
        self.state = "idle"
        return self

    def restart(self):
        return self.reset().start()

    def _tick(self, now: float):
        if self.state != "running":
            return False
        elapsed = now - self._start
        for offset, animation in self._items:
            if elapsed >= offset and animation.state == "idle":
                animation.start()
        if self._items and all(animation.state in ("completed", "cancelled") for _, animation in self._items):
            self.state = "completed"
            if self.on_complete:
                self.on_complete()
            return False
        return True
