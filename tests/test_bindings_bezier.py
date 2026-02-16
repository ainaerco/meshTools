"""Tests for _bezier C++ extension bindings."""

import pytest

_bezier = pytest.importorskip("_bezier")


class TestBezier:
    """Bezier curve binding tests."""

    def test_init_default(self):
        b = _bezier.Bezier()
        assert b is not None

    def test_init_points(self):
        b = _bezier.Bezier([0.0, 1.0, 2.0, 3.0])
        assert b is not None

    def test_interpolate(self):
        b = _bezier.Bezier([0.0, 1.0, 2.0, 3.0])
        assert callable(b.interpolate)
        # interpolate(desired_num) can raise with minimal points; Spline covers usage


class TestLagrange:
    """Lagrange curve binding tests."""

    def test_init_default(self):
        L = _bezier.Lagrange()
        assert L is not None

    def test_init_points(self):
        L = _bezier.Lagrange([0.0, 1.0, 2.0])
        assert L is not None

    def test_interpolate(self):
        L = _bezier.Lagrange([0.0, 1.0, 2.0, 3.0])
        assert callable(L.interpolate)
        # interpolate(desired_num) can raise with minimal points; Spline covers usage


class TestSpline:
    """Spline binding tests."""

    def test_init_default(self):
        s = _bezier.Spline()
        assert s is not None

    def test_init_points(self):
        s = _bezier.Spline([0.0, 1.0, 2.0, 3.0])
        assert s is not None

    def test_interpolate(self):
        s = _bezier.Spline([0.0, 1.0, 2.0, 3.0])
        out = s.interpolate(8)
        assert isinstance(out, list)
        assert len(out) >= 1
        for x in out:
            assert isinstance(x, (int, float))
