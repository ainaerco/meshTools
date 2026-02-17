"""Tests for noise module (Simplex-style procedural noise)."""

import pytest

pytest.importorskip("meshTools.noise")
from meshTools.noise import Noise


class TestNoise:
    """Smoke tests for Noise (snoise and related)."""

    def test_snoise_4d(self):
        """Noise().snoise(x, y, z, t) returns a scalar in [-1, 1]."""
        n = Noise()
        val = n.snoise(0.2, 0.2, 0.1, 0.8)
        assert isinstance(val, (int, float))
        assert -1 <= val <= 1

    def test_snoise_3d(self):
        """Noise().snoise(x, y, z) returns a scalar."""
        n = Noise()
        val = n.snoise(0.1, 0.2, 0.3)
        assert isinstance(val, (int, float))
        assert -1 <= val <= 1
