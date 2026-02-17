"""Maya-only script: triangulate first face of selected mesh and add tris. Disabled for CI."""

import pytest

pytestmark = pytest.mark.skip(reason="Maya-only; run manually inside Maya")


def test_triangulate_face_in_maya():
    import maya.OpenMaya as OpenMaya
    from meshTools.maya import MayaMesh
    from meshTools.geometry import Vector, Polygon

    selectionList = OpenMaya.MSelectionList()
    dagPath = OpenMaya.MDagPath()
    OpenMaya.MGlobal.getActiveSelectionList(selectionList)
    selectionList.getDagPath(0, dagPath)
    name = dagPath.fullPathName()
    m = MayaMesh(dag=dagPath, vertices=1, faces=1, edges=1, normals=1)
    fs = m.faces[0]
    vs = [Vector(m.vertices[f].x, m.vertices[f].y, m.vertices[f].z) for f in fs]
    n = Vector(0, 1, 0)
    p = Polygon(vs, fs, n)
    tri = p.triangulate()
    tris = []
    for i in range(len(tri) // 3):
        tris += [[tri[i * 3], tri[i * 3 + 1], tri[i * 3 + 2]]]
    m.addFaces(tris)
    m.meshToMaya(name="low_" + name)
