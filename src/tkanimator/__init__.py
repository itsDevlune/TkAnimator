"""TkAnimator: event-loop-safe animation primitives for Tkinter."""
from .adapters.canvas import move_item, rotate_image
from .animations import (
    bounce,
    color_transition,
    expand_shrink,
    fade_toplevel,
    follow_path,
    pulse,
    scroll,
    shake,
    slide,
)
from .core.animation import Animation, Tween
from .core.animator import Animator
from .core.easing import Easing, EasingFunction
from .core.timeline import Timeline
from .sequences.sequence import Parallel, Sequence, stagger

__version__ = "2.0.0"
__all__ = [
    "Animation", "Animator", "Easing", "EasingFunction", "Parallel", "Sequence", "Timeline", "Tween",
    "bounce", "color_transition", "expand_shrink", "fade_toplevel", "follow_path", "move_item", "pulse",
    "rotate_image", "scroll", "shake", "slide", "stagger",
]
