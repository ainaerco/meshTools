"""Tests for chull module (convex hull)."""

import pytest

pytest.importorskip("meshTools.chull")
from meshTools.chull import Hull
from meshTools.geometry import Vector


class TestHull:
    """Smoke tests for Hull (convex hull of 3D point set)."""

    def test_hull_cube(self):
        """Hull of unit cube vertices returns faces and vertices via exportHull."""
        cube = [
            Vector(0, 0, 0),
            Vector(1, 0, 0),
            Vector(0, 1, 0),
            Vector(1, 1, 0),
            Vector(0, 0, 1),
            Vector(1, 0, 1),
            Vector(0, 1, 1),
            Vector(1, 1, 1),
        ]
        h = Hull(cube)
        faces, vertices = h.exportHull()
        assert isinstance(faces, list)
        assert isinstance(vertices, list)
        assert len(vertices) >= 4
        assert len(faces) >= 4

    def test_hull_tetrahedron(self):
        """Hull of tetrahedron is the tetrahedron."""
        tetrahedron = [
            Vector(0, 0, 0),
            Vector(1, 0, 0),
            Vector(0, 1, 0),
            Vector(1, 1, 1),
        ]
        h = Hull(tetrahedron)
        faces, vertices = h.exportHull()
        assert len(vertices) == 4
        assert len(faces) == 4
