"""Canvas and image helpers for TkAnimator."""
from __future__ import annotations

import tkinter as tk

from ..core.animation import Animation


def move_item(canvas: tk.Canvas, item: int | str, x: float, y: float, **options) -> Animation:
    """Animate a Canvas item center to coordinates (Canvas-native rendering)."""
    coords = canvas.coords(item)
    bbox = canvas.bbox(item)
    if not coords or bbox is None:
        raise ValueError(f"Canvas item {item!r} is missing or has no bounds")
    sx, sy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
    original = coords[:]

    def update(progress: float) -> None:
        dx, dy = (x - sx) * progress, (y - sy) * progress
        canvas.coords(item, *(value + (dx if index % 2 == 0 else dy) for index, value in enumerate(original)))

    return Animation(canvas, update, conflict_key=("canvas-item", item), **options)


def rotate_image(canvas: tk.Canvas, item: int | str, image, angle: float, *, duration: float = 500, **options) -> Animation:
    """Rotate a Canvas image item using Pillow; return its animation handle.

    Pillow is optional and only required when this helper is called. The caller
    should retain the original ``PhotoImage`` reference for as long as needed.
    """
    try:
        from PIL import Image, ImageTk
    except ImportError as exc:
        raise RuntimeError("rotate_image requires Pillow; install tk-animator[images]") from exc
    if not isinstance(image, Image.Image):
        raise TypeError("image must be a Pillow Image")
    center = canvas.coords(item)
    if len(center) < 2:
        raise ValueError("Canvas image item has no position")
    original = image.copy()
    refs: dict[str, object] = {}

    def update(progress: float) -> None:
        rendered = ImageTk.PhotoImage(original.rotate(angle * progress, resample=Image.Resampling.BICUBIC, expand=False))
        refs["current"] = rendered
        canvas.itemconfigure(item, image=rendered)

    def finish() -> None:
        final = ImageTk.PhotoImage(original.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False))
        refs["final"] = final
        canvas.itemconfigure(item, image=final)

    return Animation(canvas, update, duration=duration, on_complete=finish,
                     conflict_key=("canvas-image", item), on_cancel=finish, **options)
