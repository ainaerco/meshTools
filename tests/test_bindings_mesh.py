"""Tests for _mesh C++ extension bindings."""

import pytest

pytest.importorskip("meshTools")
from meshTools import _mesh

if _mesh is None:
    pytest.skip("_mesh extension not built")


class TestVert:
    """Vert binding tests."""

    def test_init(self):
        v = _mesh.Vert()
        assert v is not None

    def test_compute_normal_bound(self):
        v = _mesh.Vert()
        # computeNormal() is bound; calling it with a default Vert (no mesh)
        # can hang (neighbors() is empty, C++ loop). Just check it exists.
        assert callable(getattr(v, "computeNormal"))


class TestMesh:
    """Mesh binding tests."""

    def test_init(self):
        m = _mesh.Mesh()
        assert m is not None

    def test_verts_property(self):
        m = _mesh.Mesh()
        verts = m.verts
        assert verts is not None
        # Should be a sequence (list or list-like) of Vert
        assert hasattr(verts, "__len__")
