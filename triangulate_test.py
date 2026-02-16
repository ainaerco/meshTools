import maya.OpenMaya as OpenMaya
from mesh_maya import MayaMesh
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
for i in range(len(tri) / 3):
    tris += [[tri[i * 3], tri[i * 3 + 1], tri[i * 3 + 2]]]
m.addFaces(tris)
ret = m.meshToMaya(name="low_" + name)
print(fs)
for i in range(len(fs)):
    last = i + 1
    if i == len(fs) - 1:
        last = 0
    e0 = m.vertices[fs[i]] - m.vertices[fs[i - 1]]
    e1 = m.vertices[fs[last]] - m.vertices[fs[i]]
    print(fs[i], n.dot(e0.cross(e1)), e0.cross(e1).lengthSquared())
# m.triangulate([0])
# ret = m.meshToMaya(name = 'low_'+name)
