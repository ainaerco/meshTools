import math
import random

import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

from meshTools.geometry import BBox, Point, Transform, Vector, pointInPoly
from meshTools.maya.mesh import MayaMesh


def tileScatter(
    self,
    copy_type="duplicate",
    pattern="even",
    align_axis=1,
    srandom_rotate=Point(),
    srandom_translate=Point(),
    srandom_scale=Point(),
    facing_sun=0.0,
):
    """copy_type = duplicate instance combine"""
    """ pattern = even straight """
    selectionList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selectionList)

    tileDAG = OpenMaya.MDagPath()
    selectionList.getDagPath(1, tileDAG)
    # print tileDAG.fullPathName()
    meshFn = OpenMaya.MFnMesh(tileDAG)
    bbox = meshFn.boundingBox()

    tile_bbox = BBox(
        min=Vector(bbox.min().x, bbox.min().y, bbox.min().z),
        max=Vector(bbox.max().x, bbox.max().y, bbox.max().z),
    )
    if copy_type == "combine":
        tile_mesh = MayaMesh(dag=tileDAG)
        combine_tile_mesh = MayaMesh(dag=tileDAG, empty=1)
    else:
        tiles_group = cmds.group(empty=True, name="tile_scatter")
    for face in range(len(self.faces)):
        # print face,self.faces[face]
        maxy = self.vertices[self.faces[face][0]][align_axis]
        maxid1 = self.faces[face][0]
        face_vertices = []
        for i in range(len(self.faces[face])):
            vert = self.vertices[self.faces[face][i]]
            face_vertices += [Point(vert.x, vert.y, vert.z)]
            newy = vert[align_axis]
            if newy > maxy:
                maxy = newy
                maxid1 = self.faces[face][i]
        neighbors = self.findVertexNeighbor(maxid1, [face])
        maxy = self.vertices[neighbors[0]][align_axis]
        maxid2 = neighbors[0]
        for neighbor in neighbors:
            newy = self.vertices[neighbor][align_axis]
            if newy > maxy:
                maxy = newy
                maxid2 = neighbor
        normal = self.getNormal(face)
        edge = self.vertices[maxid2] - self.vertices[maxid1]

        oriented = Transform()
        oriented.from2Vectors(edge, normal)
        t_lookat = Transform()
        t_lookat.lookAt(Point(), edge, normal)

        for i in range(len(self.faces[face])):
            face_vertices[i] = oriented.applyTransform(face_vertices[i])

            # print face_vertices[i]
            # self.addVertex(face_vertices[i])
            if i == 0:
                minx = face_vertices[0].x
                maxx = face_vertices[0].x
                miny = face_vertices[0].y
                maxy = face_vertices[0].y
                z = face_vertices[0].z
            else:
                minx = min(minx, face_vertices[i].x)
                maxx = max(maxx, face_vertices[i].x)
                miny = min(miny, face_vertices[i].y)
                maxy = max(maxy, face_vertices[i].y)
        # self.addVertex(Point(minx,miny,z+0.3))
        # self.addVertex(Point(maxx,maxy,z+0.3))

        countx = int((maxx - minx) / float(tile_bbox[1].z - tile_bbox[0].z))
        county = int((maxy - miny) / float(tile_bbox[1].x - tile_bbox[0].x))
        if countx == 0 or county == 0:
            continue

        stepx = tile_bbox[1].z - tile_bbox[0].z
        stepy = tile_bbox[1].x - tile_bbox[0].x

        oriented.invert()

        enlarge = Transform()
        enlarge.scaleLocal(
            Vector(
                (maxx - minx + stepx) / float(maxx - minx) * 5,
                (maxy - miny + stepy) / float(maxy - miny) * 5,
                1,
            ),
            Vector(maxx * 0.5 + minx * 0.5, maxy * 0.5 + miny * 0.5, 0),
        )
        for i in range(len(face_vertices)):
            face_vertices[i] = enlarge.applyTransform(face_vertices[i])
            # self.addVertex(face_vertices[i])

        if copy_type == "duplicate" or copy_type == "instance":
            tile_group = cmds.group(empty=True, name="tile" + str(face))
            cmds.parent(tile_group, tiles_group, relative=True)
        for i in range(countx + 1):
            random_translate = Point(
                random.uniform(-srandom_translate.x, srandom_translate.x),
                random.uniform(-srandom_translate.y, srandom_translate.y),
                random.uniform(-srandom_translate.z, srandom_translate.z),
            )
            # print random_translate
            for j in range(county + 1):
                random_rotate = Point(
                    random.uniform(-srandom_rotate.x, srandom_rotate.x),
                    random.uniform(-srandom_rotate.y, srandom_rotate.y),
                    random.uniform(-srandom_rotate.z, srandom_rotate.z),
                )

                if pattern == "even" and j % 2:
                    newPoint = Point(
                        stepx * 0.5 + minx + stepx * i + random_translate.x,
                        miny + stepy * j + random_translate.y,
                        z + random_translate.z,
                    )
                    self.addVertex(newPoint)
                    if not pointInPoly(newPoint, face_vertices):
                        continue
                    newPoint = oriented.applyTransform(
                        Point(
                            stepx * 0.5 + minx + stepx * i + random_translate.x,
                            miny + stepy * j + random_translate.y,
                            z + random_translate.z,
                        )
                    )

                if (pattern == "even" and not j % 2) or pattern == "straight":
                    newPoint = Point(
                        minx + stepx * i + random_translate.x,
                        miny + stepy * j + random_translate.y,
                        z + random_translate.z,
                    )
                    self.addVertex(newPoint)
                    if not pointInPoly(newPoint, face_vertices):
                        continue
                    newPoint = oriented.applyTransform(
                        Point(
                            minx + stepx * i + random_translate.x,
                            miny + stepy * j + random_translate.y,
                            z + random_translate.z,
                        )
                    )

                rot = t_lookat.getEuler()
                if copy_type == "duplicate" or copy_type == "instance":
                    if copy_type == "duplicate":
                        newObjectDAG = cmds.duplicate(
                            tileDAG.fullPathName(), ic=0
                        )
                    else:
                        newObjectDAG = cmds.instance(tileDAG.fullPathName())
                    scalePivot = cmds.xform(
                        newObjectDAG, query=True, ws=True, sp=True
                    )
                    transform = cmds.xform(
                        newObjectDAG, query=True, ws=True, t=True
                    )
                    cmds.xform(
                        newObjectDAG,
                        t=(
                            (transform[0] - scalePivot[0]) + newPoint.x,
                            (transform[1] - scalePivot[1]) + newPoint.y,
                            (transform[2] - scalePivot[2]) + newPoint.z,
                        ),
                    )
                    cmds.rotate(
                        math.degrees(rot.x) + random_rotate.x,
                        math.degrees(rot.y) + random_rotate.y,
                        math.degrees(rot.z) + random_rotate.z,
                        newObjectDAG,
                        os=True,
                        r=True,
                        rotateXYZ=True,
                    )
                    cmds.parent(newObjectDAG, tile_group, relative=True)
                if copy_type == "combine":
                    t_final = Transform()
                    t_final.translate(newPoint)
                    tx, ty, tz = Transform(), Transform(), Transform()
                    if facing_sun != 0.0:
                        rot = rot.lerp(Vector(), facing_sun)
                    tx.rotateX(rot.x + random_rotate.x / 50.0)
                    ty.rotateY(rot.y + random_rotate.y / 50.0)
                    tz.rotateZ(rot.z + random_rotate.z / 50.0)
                    t_final = t_final * tx * ty * tz
                    combine_tile_mesh.multiDuplicateTransform(
                        tile_mesh, t_final
                    )
        # end copy for
    if copy_type == "combine":
        combine_tile_mesh.meshToMaya()
    # end face for

    # self.meshToMaya()
