"""Value interpolation helpers."""
from __future__ import annotations

from itertools import pairwise
from typing import TypeVar

T = TypeVar("T", int, float)


def interpolate(start: T, end: T, progress: float) -> T:
    """Linearly interpolate numeric values, preserving integral outputs when possible."""
    value = start + (end - start) * progress
    if isinstance(start, int) and isinstance(end, int):
        return round(value)  # type: ignore[return-value]
    return value  # type: ignore[return-value]


def interpolate_color(start: str, end: str, progress: float) -> str:
    """Interpolate Tk-compatible #RRGGBB colors."""
    a, b = _rgb(start), _rgb(end)
    channels = [round(x + (y - x) * progress) for x, y in zip(a, b)]
    return "#" + "".join(f"{c:02x}" for c in channels)


def interpolate_path(points: list[tuple[float, float]], progress: float) -> tuple[float, float]:
    """Interpolate along a polyline, distributing progress by segment length."""
    if len(points) < 2:
        raise ValueError("a path needs at least two points")
    lengths = [((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** .5 for a, b in pairwise(points)]
    total = sum(lengths)
    if total == 0:
        return points[-1]
    distance = min(1.0, max(0.0, progress)) * total
    for ((x1, y1), (x2, y2)), length in zip(pairwise(points), lengths):
        if distance <= length:
            ratio = 0.0 if length == 0 else distance / length
            return x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio
        distance -= length
    return points[-1]


def _rgb(color: str) -> tuple[int, int, int]:
    if len(color) != 7 or not color.startswith("#"):
        raise ValueError("color must use #RRGGBB format")
    try:
        return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))  # type: ignore[return-value]
    except ValueError as exc:
        raise ValueError(f"invalid color: {color!r}") from exc
