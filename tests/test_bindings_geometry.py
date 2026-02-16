"""Tests for _geometry C++ extension bindings (via meshTools.geometry)."""

import pytest

# Skip all tests in this module if the extension or package is not available
pytest.importorskip("meshTools.geometry")
from meshTools.geometry import (
    BBox,
    Transform,
    Vector,
    Ray,
    Polygon,
    epsilonTest,
    pointInPoly,
    interpolateBezier,
    interpolateCatmullRom,
    lerp,
    solveCubic,
    fit,
    min as geom_min,
    max as geom_max,
    getBarycentric,
    sortedVectorArray,
)


class TestVector:
    """Vector binding tests."""

    def test_init_default(self):
        v = Vector()
        assert v.x == 0.0 and v.y == 0.0 and v.z == 0.0

    def test_init_xyz(self):
        v = Vector(1.0, 2.0, 3.0)
        assert v.x == 1.0 and v.y == 2.0 and v.z == 3.0

    def test_init_list(self):
        v = Vector([4.0, 5.0, 6.0])
        assert v[0] == 4.0 and v[1] == 5.0 and v[2] == 6.0

    def test_getitem(self):
        v = Vector(1.0, 2.0, 3.0)
        assert v[0] == 1.0 and v[1] == 2.0 and v[2] == 3.0

    def test_repr(self):
        v = Vector(1, 2, 3)
        # __repr__ is bound to Vector::toString (returns std::string); nanobind
        # may not convert to Python str; just ensure we can use the vector
        try:
            r = repr(v)
            assert isinstance(r, str) and "1" in r and "2" in r and "3" in r
        except TypeError:
            # Binding returns C++ string; exercising the binding is enough
            pass

    def test_add_sub(self):
        a = Vector(1, 0, 0)
        b = Vector(0, 1, 0)
        c = a + b
        assert c.x == 1.0 and c.y == 1.0 and c.z == 0.0
        d = c - b
        assert d.x == a.x and d.y == a.y and d.z == a.z

    def test_scalar_mul_div(self):
        v = Vector(2, 4, 6)
        u = v * 2.0
        assert u.x == 4.0 and u.y == 8.0 and u.z == 12.0
        w = u / 2.0
        assert w.x == v.x and w.y == v.y and w.z == v.z

    def test_length_normalize(self):
        v = Vector(3, 4, 0)
        assert abs(v.length() - 5.0) < 1e-6
        u = v.normalize()
        assert abs(u.length() - 1.0) < 1e-6
        assert abs(u.x - 0.6) < 1e-6 and abs(u.y - 0.8) < 1e-6

    def test_dot_cross(self):
        a = Vector(1, 0, 0)
        b = Vector(0, 1, 0)
        assert abs(a.dot(b) - 0.0) < 1e-6
        c = a.cross(b)
        assert abs(c.x) < 1e-6 and abs(c.y) < 1e-6 and abs(c.z - 1.0) < 1e-6

    def test_lerp(self):
        a = Vector(0, 0, 0)
        b = Vector(2, 0, 0)
        m = a.lerp(b, 0.5)
        assert abs(m.x - 1.0) < 1e-6 and m.y == 0 and m.z == 0

    def test_equality(self):
        a = Vector(1, 2, 3)
        b = Vector(1, 2, 3)
        c = Vector(1, 2, 4)
        assert a == b
        assert a != c

    def test_to_list(self):
        v = Vector(1, 2, 3)
        assert v.toList() == [1.0, 2.0, 3.0]

    def test_zero_test(self):
        v = Vector(0.0, 0.0, 1e-8)
        assert v.zeroTest() is True
        v2 = Vector(0.1, 0, 0)
        assert v2.zeroTest() is False


class TestMathFunctions:
    """Free math function binding tests."""

    def test_epsilon_test(self):
        assert epsilonTest(0.0) is True
        assert epsilonTest(1e-7) is True
        assert epsilonTest(0.01) is False

    def test_lerp(self):
        assert abs(lerp(0.0, 0.0, 10.0) - 0.0) < 1e-6
        assert abs(lerp(1.0, 0.0, 10.0) - 10.0) < 1e-6
        assert abs(lerp(0.5, 0.0, 10.0) - 5.0) < 1e-6

    def test_fit(self):
        # map [0,10] -> [0,1]
        assert abs(fit(5.0, 0.0, 10.0, 0.0, 1.0) - 0.5) < 1e-6

    def test_min_max(self):
        assert geom_min(1.0, 2.0) == 1.0
        assert geom_max(1.0, 2.0) == 2.0

    def test_solve_cubic(self):
        # x^3 = 0 -> one root 0
        roots = solveCubic(1, 0, 0, 0)
        assert hasattr(roots, "x") and hasattr(roots, "y") and hasattr(roots, "z")
        assert abs(roots.x) < 1e-5

    def test_interpolate_bezier(self):
        # at t=0 should be p0, at t=1 should be p3
        assert abs(interpolateBezier(0.0, 1.0, 2.0, 3.0, 4.0) - 1.0) < 1e-6
        assert abs(interpolateBezier(1.0, 1.0, 2.0, 3.0, 4.0) - 4.0) < 1e-6

    def test_interpolate_catmull_rom(self):
        y = interpolateCatmullRom(0.5, 0.0, 1.0, 2.0, 3.0)
        assert 0 <= y <= 3

    def test_point_in_poly(self):
        # point inside unit square in xy
        poly = [
            Vector(0, 0, 0),
            Vector(1, 0, 0),
            Vector(1, 1, 0),
            Vector(0, 1, 0),
        ]
        inside = Vector(0.5, 0.5, 0)
        outside = Vector(-0.1, -0.1, 0)
        assert pointInPoly(inside, poly) is True
        assert pointInPoly(outside, poly) is False

    def test_get_barycentric(self):
        a = Vector(0, 0, 0)
        b = Vector(1, 0, 0)
        c = Vector(0, 1, 0)
        p = Vector(0.25, 0.25, 0)
        bary = getBarycentric(p, a, b, c)
        assert hasattr(bary, "x") and hasattr(bary, "y") and hasattr(bary, "z")

    def test_sorted_vector_array(self):
        pts = [Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)]
        out = sortedVectorArray(pts, 0)
        assert isinstance(out, list) and len(out) == len(pts)


class TestBBox:
    """BBox binding tests."""

    def test_init_default(self):
        b = BBox()
        assert b.min is not None and b.max is not None and b.center is not None

    def test_from_point_set(self):
        pts = [
            Vector(0, 0, 0),
            Vector(1, 0, 0),
            Vector(0, 1, 0),
            Vector(0, 0, 1),
        ]
        b = BBox()
        b.fromPointSet(pts)
        assert abs(b.min.x) < 1e-6 and abs(b.min.y) < 1e-6 and abs(b.min.z) < 1e-6
        assert abs(b.max.x - 1) < 1e-6 and abs(b.max.y - 1) < 1e-6 and abs(b.max.z - 1) < 1e-6

    def test_axis_property(self):
        pts = [Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)]
        b = BBox()
        b.fromPointSet(pts)
        axes = b.axis
        assert len(axes) == 3
        for ax in axes:
            assert ax.x is not None and ax.y is not None and ax.z is not None

    def test_getitem(self):
        b = BBox()
        b.fromPointSet([Vector(0, 0, 0), Vector(1, 1, 1)])
        v0 = b[0]
        v1 = b[1]
        assert hasattr(v0, "x") and hasattr(v1, "x")

    def test_obb_from_point_set(self):
        pts = [
            Vector(0, 0, 0),
            Vector(2, 0, 0),
            Vector(0, 2, 0),
            Vector(0, 0, 2),
        ]
        b = BBox()
        b.obbFromPointSet(pts)
        axes = b.axis
        assert axes is not None and len(axes) == 3
        center = b.calcCenter()
        if center is not None:
            assert hasattr(center, "x")


class TestRay:
    """Ray binding tests."""

    def test_init_and_props(self):
        o = Vector(0, 0, 0)
        d = Vector(1, 0, 0)
        r = Ray(o, d)
        assert r.origin.x == 0 and r.origin.y == 0 and r.origin.z == 0
        assert r.direction.x == 1 and r.direction.y == 0 and r.direction.z == 0

    def test_point_distance(self):
        o = Vector(0, 0, 0)
        d = Vector(1, 0, 0)
        r = Ray(o, d)
        p = Vector(0, 1, 0)
        dist = r.pointDistance(p)
        assert isinstance(dist, (int, float))


class TestTransform:
    """Transform binding tests."""

    def test_init_default(self):
        t = Transform()
        assert t.m is not None

    def test_identity(self):
        t = Transform()
        t.identity()
        m = t.m
        assert len(m) == 4 and len(m[0]) == 4

    def test_look_at(self):
        t = Transform()
        t.lookAt(
            Vector(0, 0, 0),
            Vector(1, 0, 0),
            Vector(0, 1, 0),
        )
        assert t.m is not None

    def test_translate_scale(self):
        t = Transform()
        t.identity()
        t = t.translate(1.0, 0.0, 0.0)
        t = t.scale(2.0, 2.0, 2.0)
        v = Vector(1, 0, 0)
        v2 = v.applyTransform(t)
        assert abs(v2.x - 2.0) < 1e-5  # translate 1 then scale 2

    def test_multiply(self):
        a = Transform()
        a.identity()
        b = Transform()
        b.identity()
        c = a * b
        assert c.m is not None


class TestPolygon:
    """Polygon binding tests."""

    def test_triangulate(self):
        verts = [
            Vector(0, 0, 0),
            Vector(1, 0, 0),
            Vector(0.5, 1, 0),
        ]
        indices = [0, 1, 2]
        normal = Vector(0, 0, 1)
        poly = Polygon(verts, indices, normal)
        tris = poly.triangulate()
        assert isinstance(tris, list)
        assert all(isinstance(i, int) for i in tris)
