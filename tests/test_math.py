import pytest

from tkanimator import Easing
from tkanimator.core.interpolation import interpolate, interpolate_color, interpolate_path


@pytest.mark.parametrize("curve", list(Easing))
def test_easing_endpoints(curve):
    assert curve(0) == pytest.approx(0)
    assert curve(1) == pytest.approx(1)


def test_interpolation():
    assert interpolate(10, 20, .5) == 15
    assert interpolate_color("#000000", "#ffffff", .5) == "#808080"
    assert interpolate_path([(0, 0), (3, 0), (3, 4)], .5) == pytest.approx((3, 0.5))
    assert interpolate_path([(0, 0), (0, 0)], .5) == (0, 0)


def test_path_rejects_single_point():
    with pytest.raises(ValueError):
        interpolate_path([(1, 1)], .5)


@pytest.mark.parametrize("color", ["fff", "#xyzxyz", "123456"])
def test_invalid_color(color):
    with pytest.raises(ValueError):
        interpolate_color(color, "#ffffff", .5)
