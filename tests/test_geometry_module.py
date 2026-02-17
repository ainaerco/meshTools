"""Tests for geometry module (BBox, Transform, Vector, etc.)."""

from random import random

import pytest

pytest.importorskip("meshTools.geometry")
from meshTools.geometry import BBox, Transform, Vector, epsilonTest, solveCubic


class TestGeometryModule:
    """Smoke and behaviour tests for geometry bindings."""

    def test_vector_and_epsilon(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(0.00001, 0, 0)
        assert v2.zeroTest() is not None
        assert epsilonTest(0.01) is not None
        assert v1.x == 1.0

    def test_bbox_from_point_set(self):
        z = [Vector(random(), random(), random()) for _ in range(10)]
        b = BBox()
        b.fromPointSet(z)
        assert b[0][0] is not None

    def test_solve_cubic(self):
        result = solveCubic(5, 6, 1, 0)
        assert result is not None

    def test_bbox_obb_from_point_set(self):
        verts_f = [Vector(3.32413094384e-07, -2.5349085331, -2.5349085331)]
        verts_f += [Vector(-2.5349085331, -2.5349085331, -2.216087438e-07)]
        verts_f += [Vector(-1.108043719e-07, -2.5349085331, 2.5349085331)]
        verts_f += [Vector(2.5349085331, -2.5349085331, 0.0)]
        verts_f += [Vector(4.70103117323e-07, 0.0, -3.58490204811)]
        verts_f += [Vector(-3.58490204811, 0.0, -3.13402097163e-07)]
        verts_f += [Vector(-1.56701048581e-07, 0.0, 3.58490204811)]
        verts_f += [Vector(3.58490204811, 0.0, 0.0)]
        verts_f += [Vector(3.32413094384e-07, 2.5349085331, -2.5349085331)]
        verts_f += [Vector(-2.5349085331, 2.5349085331, -2.216087438e-07)]
        verts_f += [Vector(-1.108043719e-07, 2.5349085331, 2.5349085331)]
        verts_f += [Vector(2.5349085331, 2.5349085331, 0.0)]
        verts_f += [Vector(0.0, -3.58490204811, 0.0)]
        verts_f += [Vector(0.0, 3.58490204811, 0.0)]
        b = BBox()
        b.obbFromPointSet(verts_f)
        assert b.axis[0] is not None
        assert b.axis[1] is not None
        assert b.axis[2] is not None

    def test_transform_look_at_and_apply(self):
        t = Transform()
        t.lookAt(
            Vector(0, 0, 0),
            Vector(1, 1, 0).normalize(),
            Vector(0, 1, 0),
        )
        v1 = Vector(1, 0, 0)
        result = v1.applyTransform(t)
        assert result is not None
