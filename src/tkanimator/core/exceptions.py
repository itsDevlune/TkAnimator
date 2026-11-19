"""TkAnimator exception types."""

class TkAnimatorError(Exception):
    """Base exception for TkAnimator."""

class UnsupportedAnimationError(TkAnimatorError, ValueError):
    """Raised when an effect is not supported by the selected widget/backend."""
