from math import degrees

from meshTools.geometry import BBox, Transform, Vector
import maya.cmds as cmds


def perform(**kwargs):
    sel = cmds.ls(sl=True)
    sel3 = []
    for s in sel:
        sel3 += cmds.xform(s, q=True, ws=True, t=True)
    pointset = []
    for i in range(len(sel3) / 3):
        pointset += [Vector(sel3[i * 3], sel3[i * 3 + 1], sel3[i * 3 + 2])]
    bbox = BBox()
    bbox.obbFromPointSet(pointset)
    t = Transform(bbox.axis[0], bbox.axis[1], bbox.axis[2])
    t = t.transpose()
    z = t.getEuler()
    cube = cmds.createNode("polyCube")
    cubeShape = cmds.createNode("mesh")
    cubeTrans = cmds.listRelatives(cubeShape, p=True)[0]
    cmds.connectAttr(cube + ".output", cubeShape + ".inMesh")
    cmds.setAttr(cubeTrans + ".tx", bbox.center[0])
    cmds.setAttr(cubeTrans + ".ty", bbox.center[1])
    cmds.setAttr(cubeTrans + ".tz", bbox.center[2])
    cmds.setAttr(cubeTrans + ".rz", degrees(z[2]))
    cmds.setAttr(cubeTrans + ".ry", degrees(z[1]))
    cmds.setAttr(cubeTrans + ".rx", degrees(z[0]))
    cmds.setAttr(cube + ".width", bbox.max[0] - bbox.min[0])
    cmds.setAttr(cube + ".height", bbox.max[1] - bbox.min[1])
    cmds.setAttr(cube + ".depth", bbox.max[2] - bbox.min[2])
    cmds.sets(e=True, forceElement="initialShadingGroup")
    cmds.select(sel)
