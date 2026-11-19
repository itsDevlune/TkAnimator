import pytest

from tkanimator import Animation, Animator, Easing, Parallel, Sequence, Timeline


class FakeWidget:
    """Minimal scheduler host for validating public input rules without a display."""


def test_easing_is_callable_and_exports_exist():
    assert Easing.EASE_IN_OUT_CUBIC(.5) == pytest.approx(.5)
    assert all(callable(x) for x in (Animation, Animator, Parallel, Sequence, Timeline))


def test_animation_validates_options():
    with pytest.raises(ValueError):
        Animation(FakeWidget(), lambda _: None, duration=-1)
    with pytest.raises(ValueError):
        Animation(FakeWidget(), lambda _: None, repeat=-2)


def test_animator_start_requires_configuration():
    animator = Animator(FakeWidget())
    with pytest.raises(RuntimeError):
        animator.start()
