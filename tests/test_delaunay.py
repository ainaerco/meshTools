"""Tests for delaunay module (3D Delaunay tetrahedralization)."""

from random import random

import pytest

pytest.importorskip("meshTools.delaunay")
from meshTools.delaunay import Delaunay
from meshTools.geometry import Point, fit


class TestDelaunay:
    """Smoke tests for Delaunay (tetrahedralization from point set)."""

    def test_delaunay_from_random_points(self):
        """Delaunay(verts, max) builds from a small random point set."""
        verts = []
        min_val, max_val = -10, 10
        for _ in range(20):
            verts.append(
                Point(
                    fit(random(), 0, 1, min_val, max_val),
                    fit(random(), 0, 1, min_val, max_val),
                    fit(random(), 0, 1, min_val, max_val),
                )
            )
        d = Delaunay(verts, max_val)
        assert d is not None
        assert hasattr(d, "orig_vertices")
        assert len(d.orig_vertices) == 20
