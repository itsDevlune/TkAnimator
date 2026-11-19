"""Easing functions used by TkAnimator."""
from __future__ import annotations

import math
from collections.abc import Callable
from enum import Enum

EasingFunction = Callable[[float], float]


class Easing(Enum):
    """Named easing curves. Each member is a callable accepting progress in [0, 1]."""
    LINEAR = staticmethod(lambda t: t)
    EASE_IN_QUAD = staticmethod(lambda t: t * t)
    EASE_OUT_QUAD = staticmethod(lambda t: 1 - (1 - t) ** 2)
    EASE_IN_OUT_QUAD = staticmethod(lambda t: 2 * t * t if t < .5 else 1 - (-2 * t + 2) ** 2 / 2)
    EASE_IN_CUBIC = staticmethod(lambda t: t ** 3)
    EASE_OUT_CUBIC = staticmethod(lambda t: 1 - (1 - t) ** 3)
    EASE_IN_OUT_CUBIC = staticmethod(lambda t: 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2)
    EASE_IN_QUART = staticmethod(lambda t: t ** 4)
    EASE_OUT_QUART = staticmethod(lambda t: 1 - (1 - t) ** 4)
    EASE_IN_OUT_QUART = staticmethod(lambda t: 8 * t ** 4 if t < .5 else 1 - (-2 * t + 2) ** 4 / 2)
    EASE_IN_QUINT = staticmethod(lambda t: t ** 5)
    EASE_OUT_QUINT = staticmethod(lambda t: 1 - (1 - t) ** 5)
    EASE_IN_OUT_QUINT = staticmethod(lambda t: 16 * t ** 5 if t < .5 else 1 - (-2 * t + 2) ** 5 / 2)
    EASE_IN_SINE = staticmethod(lambda t: 1 - math.cos(t * math.pi / 2))
    EASE_OUT_SINE = staticmethod(lambda t: math.sin(t * math.pi / 2))
    EASE_IN_OUT_SINE = staticmethod(lambda t: -(math.cos(math.pi * t) - 1) / 2)
    EASE_IN_EXPO = staticmethod(lambda t: 0 if t == 0 else 2 ** (10 * t - 10))
    EASE_OUT_EXPO = staticmethod(lambda t: 1 if t == 1 else 1 - 2 ** (-10 * t))
    EASE_IN_OUT_EXPO = staticmethod(lambda t: t if t in (0, 1) else 2 ** (20 * t - 10) / 2 if t < .5 else (2 - 2 ** (-20 * t + 10)) / 2)
    EASE_IN_CIRC = staticmethod(lambda t: 1 - math.sqrt(1 - t * t))
    EASE_OUT_CIRC = staticmethod(lambda t: math.sqrt(1 - (t - 1) ** 2))
    EASE_IN_OUT_CIRC = staticmethod(lambda t: (1 - math.sqrt(1 - (2 * t) ** 2)) / 2 if t < .5 else (math.sqrt(1 - (-2 * t + 2) ** 2) + 1) / 2)
    EASE_OUT_BACK = staticmethod(lambda t: 1 + 2.70158 * (t - 1) ** 3 + 1.70158 * (t - 1) ** 2)
    EASE_OUT_ELASTIC = staticmethod(lambda t: t if t in (0, 1) else 2 ** (-10 * t) * math.sin((t * 10 - .75) * (2 * math.pi / 3)) + 1)
    EASE_OUT_BOUNCE = staticmethod(lambda t: _bounce(t))
    EASE_OUT_SPRING = staticmethod(lambda t: 1 - math.exp(-7 * t) * math.cos(10 * t))

    def __call__(self, t: float) -> float:
        return self.value(t)


def _bounce(t: float) -> float:
    n, d = 7.5625, 2.75
    if t < 1 / d:
        return n * t * t
    if t < 2 / d:
        t -= 1.5 / d
        return n * t * t + .75
    if t < 2.5 / d:
        t -= 2.25 / d
        return n * t * t + .9375
    t -= 2.625 / d
    return n * t * t + .984375


def resolve_easing(easing: EasingFunction | Easing) -> EasingFunction:
    fn = easing.value if isinstance(easing, Easing) else easing
    if not callable(fn):
        raise TypeError("easing must be callable")
    return fn
