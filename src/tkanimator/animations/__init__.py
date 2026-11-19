"""Built-in practical Tk widget effects."""
from __future__ import annotations

import math
import tkinter as tk
from math import isfinite

from ..core.animation import Animation
from ..core.animator import Animator
from ..core.easing import Easing
from ..core.interpolation import interpolate_color, interpolate_path


def _geometry(widget: tk.Misc) -> tuple[float, float, dict[str, str]]:
    if widget.winfo_manager() != "place":
        raise ValueError("geometry effects require place() geometry management")
    info = widget.place_info()  # type: ignore[attr-defined]
    return float(info.get("x", widget.winfo_x())), float(info.get("y", widget.winfo_y())), info


def _positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")


def move(widget: tk.Misc, x: float | None = None, y: float | None = None, **options) -> Animation:
    return Animator(widget).move(x=x, y=y, **options)


def follow_path(widget: tk.Misc, points: list[tuple[float, float]], **options) -> Animation:
    """Move a placed widget along a polyline, proportionally to segment length."""
    _geometry(widget)
    if len(points) < 2:
        raise ValueError("path needs at least two points")
    if any(not isfinite(value) for point in points for value in point):
        raise ValueError("path coordinates must be finite")
    def update(progress: float) -> None:
        x, y = interpolate_path(points, progress)
        widget.place_configure(x=round(x), y=round(y))  # type: ignore[attr-defined]
    return Animation(widget, update, conflict_key=("geometry", "x", "y"), **options)


def slide(widget: tk.Misc, direction: str = "right", distance: float = 100, **options) -> Animation:
    directions = {"left": (-distance, 0), "right": (distance, 0), "up": (0, -distance), "down": (0, distance)}
    if direction not in directions:
        raise ValueError("direction must be left, right, up, or down")
    x, y, _ = _geometry(widget)
    dx, dy = directions[direction]
    return move(widget, x=x + dx, y=y + dy, **options)


def shake(widget: tk.Misc, intensity: float = 10, shakes: int = 5, duration: float = 800, **options) -> Animation:
    _positive("intensity", intensity)
    _positive("shakes", shakes)
    x, y, _ = _geometry(widget)
    def update(p: float) -> None:
        widget.place_configure(x=round(x + math.sin(p * shakes * 2 * math.pi) * intensity * (1-p)), y=round(y))  # type: ignore[attr-defined]
    def restore() -> None:
        widget.place_configure(x=round(x), y=round(y))  # type: ignore[attr-defined]
    return Animation(widget, update, duration=duration, easing=Easing.LINEAR, on_complete=restore,
                     conflict_key=("geometry", "x"), **options)


def bounce(widget: tk.Misc, height: float = 30, bounces: int = 3, duration: float = 1500, **options) -> Animation:
    _positive("height", height)
    _positive("bounces", bounces)
    x, y, _ = _geometry(widget)
    def update(p: float) -> None:
        widget.place_configure(x=round(x), y=round(y - abs(math.sin(p * bounces * math.pi)) * height * (1-p)))  # type: ignore[attr-defined]
    def restore() -> None:
        widget.place_configure(x=round(x), y=round(y))  # type: ignore[attr-defined]
    return Animation(widget, update, duration=duration, easing=Easing.LINEAR, on_complete=restore,
                     conflict_key=("geometry", "y"), **options)


def pulse(widget: tk.Misc, scale_factor: float = 1.2, pulses: int = 3, duration: float = 1000, **options) -> Animation:
    x, y, _info = _geometry(widget)
    width, height = widget.winfo_width(), widget.winfo_height()
    if width <= 1 or height <= 1:
        widget.update_idletasks()
        width, height = widget.winfo_width(), widget.winfo_height()
    if not isfinite(scale_factor) or scale_factor <= 0 or pulses < 1:
        raise ValueError("scale_factor must be positive and pulses must be at least 1")
    def update(p: float) -> None:
        _scale(widget, x, y, width, height, 1 + (scale_factor-1) * abs(math.sin(p*pulses*math.pi)))
    def restore() -> None:
        widget.place_configure(x=round(x), y=round(y), width=width, height=height)  # type: ignore[attr-defined]
    return Animation(widget, update, duration=duration, easing=Easing.LINEAR, on_complete=restore,
                     conflict_key=("geometry", "size"), **options)


def _scale(widget, x, y, width, height, scale):
    nw, nh = round(width*scale), round(height*scale)
    widget.place_configure(x=round(x-(nw-width)/2), y=round(y-(nh-height)/2), width=nw, height=nh)  # type: ignore[attr-defined]


def expand_shrink(widget: tk.Misc, expand_factor: float = 1.5, duration: float = 1000, shrink_back: bool = True, **options) -> Animation:
    x, y, _ = _geometry(widget)
    width, height = widget.winfo_width(), widget.winfo_height()
    if width <= 1 or height <= 1:
        widget.update_idletasks()
        width, height = widget.winfo_width(), widget.winfo_height()
    if not isfinite(expand_factor) or expand_factor <= 0:
        raise ValueError("expand_factor must be positive")
    def update(p):
        scale = 1 + (expand_factor-1) * (1 - abs(2*p - 1) if shrink_back else p)
        _scale(widget, x, y, width, height, scale)
    def restore() -> None:
        if shrink_back:
            _scale(widget, x, y, width, height, 1)
    return Animation(widget, update, duration=duration, easing=Easing.LINEAR,
                     on_complete=restore if shrink_back else None,
                     conflict_key=("geometry", "size"), **options)


def color_transition(widget: tk.Misc, start_color: str, end_color: str, property_name: str = "bg", **options) -> Animation:
    def update(p: float) -> None:
        widget.configure(**{property_name: interpolate_color(start_color, end_color, p)})
    return Animation(widget, update, conflict_key=("option", property_name), **options)


def scroll(canvas: tk.Canvas, *, target: float, axis: str = "y", duration: float = 500, **options) -> Animation:
    """Animate Canvas view position to a normalized fraction in [0, 1]."""
    if axis not in ("x", "y"):
        raise ValueError("axis must be 'x' or 'y'")
    if not isfinite(target) or not 0 <= target <= 1:
        raise ValueError("target must be between 0 and 1")
    getter = canvas.xview if axis == "x" else canvas.yview
    mover = canvas.xview_moveto if axis == "x" else canvas.yview_moveto
    start = getter()[0]
    def update(p: float) -> None:
        mover(start + (target - start) * p)
    return Animation(canvas, update, duration=duration, conflict_key=("canvas-view", axis), **options)


def fade_toplevel(window: tk.Toplevel | tk.Tk, fade_in: bool = True, duration: float = 1000, **options) -> Animation:
    """Fade an entire toplevel window via platform-supported -alpha; child widgets cannot be faded individually."""
    start, end = (0.0, 1.0) if fade_in else (1.0, 0.0)
    def update(p: float) -> None:
        window.attributes("-alpha", start + (end-start)*p)
    def prepare() -> None:
        window.attributes("-alpha", start)
    return Animation(window, update, duration=duration, on_start=prepare, **options)
