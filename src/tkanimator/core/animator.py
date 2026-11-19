"""High-level helpers for animating a Tk widget."""
from __future__ import annotations

import tkinter as tk
from typing import Any

from .animation import Animation
from .easing import Easing, EasingFunction
from .interpolation import interpolate_color


class Animator:
    def __init__(self, widget: tk.Misc) -> None:
        self.widget = widget
        self._animations: list[Animation] = []
        self._pending: Animation | None = None

    def tween(self, start: float, end: float, setter, **options: Any) -> Animation:
        animation = Animation(self.widget, lambda p: setter(start + (end - start) * p), **options)
        self._animations.append(animation)
        return animation

    def move(self, *, x: float | None = None, y: float | None = None, duration: float = 1000,
             easing: EasingFunction | Easing = Easing.EASE_IN_OUT_CUBIC, **options: Any) -> Animation:
        manager = self.widget.winfo_manager()
        if manager != "place":
            raise ValueError("move requires a widget managed by place(); pack/grid geometry cannot be overridden")
        info = self.widget.place_info()  # type: ignore[attr-defined]
        sx, sy = float(info.get("x", self.widget.winfo_x())), float(info.get("y", self.widget.winfo_y()))
        ex, ey = sx if x is None else x, sy if y is None else y
        def update(p: float) -> None:
            self.widget.place_configure(x=round(sx + (ex - sx) * p), y=round(sy + (ey - sy) * p))  # type: ignore[attr-defined]
        return self._add(update, duration, easing, options, conflict_key=("geometry", "x", "y"))

    def color(self, *, start: str, end: str, property_name: str = "bg", duration: float = 1000,
              easing: EasingFunction | Easing = Easing.LINEAR, **options: Any) -> Animation:
        def update(p: float) -> None:
            self.widget.configure(**{property_name: interpolate_color(start, end, p)})
        return self._add(update, duration, easing, options, conflict_key=("option", property_name))

    def _add(self, update, duration, easing, options, conflict_key=None):
        animation = Animation(self.widget, update, duration=duration, easing=easing,
                             conflict_key=conflict_key, **options)
        self._animations.append(animation)
        self._pending = animation
        return animation

    def start(self) -> Animation:
        """Start the most recently configured animation (for fluent use)."""
        if self._pending is None:
            raise RuntimeError("configure an animation before calling start()")
        animation, self._pending = self._pending, None
        return animation.start()

    def pause(self) -> None:
        for animation in self._animations:
            animation.pause()

    def resume(self) -> None:
        for animation in self._animations:
            animation.resume()

    def cancel(self) -> None:
        self.cancel_all()

    def cancel_all(self) -> None:
        for animation in self._animations:
            animation.cancel()
        self._animations.clear()
