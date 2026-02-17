"""Maya mesh integration: MFnMesh wrapper and mesh operations.

MayaMesh extends Mesh with OpenMaya MFnMesh loading/saving, Maya selection
integration, and Maya-specific operations. Requires Maya Python environment.
"""

import logging
import math
import random

import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

import meshTools.lists as lists
from meshTools.geometry import BBox, Point, Transform, Vector, pointInPoly
from meshTools.mesh import Mesh, kGeotype

logger = logging.getLogger(__name__)

# Set by script when run (see bottom of file)
selectionPath = None
sel_object = None


class MayaMesh(Mesh):
    """Mesh backed by Maya MFnMesh; loads/saves vertices, faces, normals from Maya DAG."""

    def __init__(self, **kwargs):
        super(MayaMesh, self).__init__()
        self.mode = "maya"
        if kwargs.get("empty", 0):
            return
        if "dag" in kwargs:
            dag = kwargs.get("dag")
            self.meshFn = OpenMaya.MFnMesh(dag)
        elif "mesh" in kwargs:
            self.meshFn = kwargs.get("mesh")
        else:
            logger.warning("Mesh not specified for MayaMesh")
            return
        self.selectionType = kGeotype.face
        if kwargs.get("pivot", 0):
            pivot = cmds.xform(q=True, ws=True, scalePivot=True)
            self.pivot = Vector(pivot[0], pivot[1], pivot[2])

        if kwargs.get("bbox", 0):
            selectionPath.pop()
            # print selectionPath.fullPathName()
            transform = OpenMaya.MFnTransform(selectionPath)
            m = transform.transformationMatrix()
            bbox = self.meshFn.boundingBox()
            min = bbox.min() * m
            max = bbox.max() * m
            self.bbox = BBox(
                min=Vector(min.x, min.y, min.z), max=Vector(max.x, max.y, max.z)
            )

        # start_time = time()
        if kwargs.get("vertices", 0):
            numVertices = self.meshFn.numVertices()
            verticesArray = OpenMaya.MFloatPointArray()
            self.meshFn.getPoints(verticesArray, OpenMaya.MSpace.kWorld)

            for i in range(numVertices):
                self.vertices.append(
                    Point(
                        verticesArray[i][0],
                        verticesArray[i][1],
                        verticesArray[i][2],
                    )
                )
        # elapsed_time = time() - start_time
        # print(str(elapsed_time)+" Elapsed on loading verts")

        # start_time = time()
        if kwargs.get("faces", 0):
            numPolygons = self.meshFn.numPolygons()
            polyList = OpenMaya.MIntArray()
            for i in range(numPolygons):
                self.meshFn.getPolygonVertices(i, polyList)
                self.faces += [list(polyList)]
        # elapsed_time = time() - start_time
        # print(str(elapsed_time)+" Elapsed on loading faces")

        if kwargs.get("normals", 0):
            numPolygons = self.meshFn.numPolygons()
            v = OpenMaya.MVector()
            for i in range(numPolygons):
                self.meshFn.getPolygonNormal(i, v)
                self.normals += [Vector(v.x, v.y, v.z)]

        # start_time = time()
        if kwargs.get("edges", 0):
            self.loadEdges()
        # elapsed_time = time() - start_time
        # print(str(elapsed_time)+" Elapsed on loading edges")
        if kwargs.get("build", 0):
            self.rebuildVertP()

    def loadEdges(self):
        numEdges = self.meshFn.numEdges()
        pArray = [0, 0]
        x = OpenMaya.MScriptUtil()
        x.createFromList(pArray, 2)
        y = x.asInt2Ptr()
        for i in range(0, numEdges):
            self.meshFn.getEdgeVertices(i, y)
            self.edges.append(
                [x.getInt2ArrayItem(y, 0, 0), x.getInt2ArrayItem(y, 0, 1)]
            )

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
                                stepx * 0.5
                                + minx
                                + stepx * i
                                + random_translate.x,
                                miny + stepy * j + random_translate.y,
                                z + random_translate.z,
                            )
                        )

                    if (
                        pattern == "even" and not j % 2
                    ) or pattern == "straight":
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

    def meshToMaya(self, **kwargs):
        polygonCounts_final = OpenMaya.MIntArray()
        polygonConnects_final = OpenMaya.MIntArray()

        vertexArray_final = OpenMaya.MFloatPointArray()
        uArray = OpenMaya.MFloatArray()
        vArray = OpenMaya.MFloatArray()
        uvConnects = OpenMaya.MIntArray()

        for i in range(len(self.vertices)):
            vertexArray_final.append(
                self.vertices[i].x, self.vertices[i].y, self.vertices[i].z
            )
            # uArray.append(self.vertices[i].x)
            # vArray.append(self.vertices[i].z)

        for i in self.faces:
            id = 0
            for j in i:
                if j > len(self.vertices) - 1:
                    logger.error("segmentation unknown vertex")
                else:
                    polygonConnects_final.append(j)
                id = id + 1
            polygonCounts_final.append(id)
        meshFS_n = OpenMaya.MFnMesh()

        if "parent" in kwargs:
            meshFS_n.create(
                len(self.vertices),
                len(self.faces),
                vertexArray_final,
                polygonCounts_final,
                polygonConnects_final,
                kwargs.get("parent"),
            )
        else:
            meshFS_n.create(
                len(self.vertices),
                len(self.faces),
                vertexArray_final,
                polygonCounts_final,
                polygonConnects_final,
            )

        uvs = kwargs.get("uvs", 0)
        if uvs:
            for i in range(len(self.uvs)):
                uArray.append(self.uvs[i].x)
                vArray.append(self.uvs[i].y)
            for i in self.face_uvs:
                for j in i:
                    if j > len(self.uvs) - 1:
                        logger.error("segmentation unknown uv")
                    else:
                        uvConnects.append(j)
            meshFS_n.setUVs(uArray, vArray)
            meshFS_n.assignUVs(polygonCounts_final, uvConnects)

        """
		for i in range(len(self.faces)):
			for j in range(len(self.faces[i])):
				meshFS_n.assignUV(i,j,self.faces[i][j])
		"""
        if "parent" in kwargs:
            return

        meshFS_n.updateSurface()
        cmds.sets(meshFS_n.name(), e=True, fe="initialShadingGroup")
        if "name" in kwargs:
            meshFS_n.setName(kwargs.get("name") + "Shape")
            transform = meshFS_n.parent(0)

            transform_dag = OpenMaya.MFnDagNode(transform)
            transform_dag.setName(kwargs.get("name"))
        return (transform_dag.fullPathName(), meshFS_n.fullPathName())

    def selectionToMaya(self, sel, sel_type):
        cmds.select(cl=True)
        if sel_type == "faces":
            sel_type = ".f"
        if sel_type == "vertices":
            sel_type = ".vtx"
        if sel_type == "edges":
            sel_type = ".e"
        sel = lists.to_maya_sel(sel_object + sel_type, sel)
        for s in sel:
            cmds.select(s, add=True)

    def getVertex(self, id):
        # Mesh.getVertex(self,id)
        point = OpenMaya.MPoint()
        self.meshFn.getPoint(id, point, 4)
        return Vector(point.x, point.y, point.z)

    # OpenMaya.getVertexNormal
    def updateVertex(self, id, value):
        # Mesh.updateVertex(self,id,value)
        pos = OpenMaya.MPoint()
        pos.x, pos.y, pos.z = value.x, value.y, value.z
        self.meshFn.setPoint(id, pos, OpenMaya.MSpace.kWorld)

    def __deleteFaces(self, faces):
        Mesh.deleteFaces(self, faces)
        # sel  = lists.to_maya_sel(sel_object+".f",faces)
        # cmds.delete(sel)

    def __deleteVertices(self, verts):
        Mesh.deleteVertices(self, verts)
        # sel  = lists.to_maya_sel(sel_object+".vtx",verts)
        # cmds.delete(sel)

    def addFace(self, value):
        Mesh.addFace(self, value)
        # p = OpenMaya.MPointArray()
        # for vert in value:
        #    p.append(self.vertices[vert].x,self.vertices[vert].y,self.vertices[vert].z)
        # self.meshFn.addPolygon(p,self.meshFn.numPolygons()+1)

    def updateFace(self, id, value):
        Mesh.updateFace(self, id, value)
        # p = OpenMaya.MPointArray()
        # for vert in value:
        #    p.append(self.vertices[vert].x,self.vertices[vert].y,self.vertices[vert].z)
        # self.meshFn.addPolygon(p,id)


"""
selectionList = OpenMaya.MSelectionList()
OpenMaya.MGlobal.getActiveSelectionList(selectionList)
selectionPath = OpenMaya.MDagPath()
selectionList.getDagPath(0, selectionPath)
selection1 = OpenMaya.MDagPath()
selectionList.getDagPath(1, selection1)

start_time = time()
t = MayaTube(curveDag=selectionPath,profileDag = selection1,reverse=0,cylinder_segments=0,taper=1)

#m = MayaMesh(dag = selectionPath,vertices=1,faces=1,edges=1)
elapsed_time = time() - start_time
logger.info("%s Elapsed on loading to mesh class", elapsed_time)
#print m
#m.test()
#m.meshToMaya(name = 'proxy')
"""
"""
sl = cmds.ls(sl=True)
sel_object = sl[0].split('.')[0]

pat = re.compile("\[\d+:\d+\]|\[\d+]")
selection_range = [[int(y) for y in pat.search(x).group(0)[1:-1].split(":")] for x in sl if pat.search(x)]
selection = []
for i in selection_range:
	if len(i)==1:
		selection.extend(i)
	else:
		for j in range(0,i[1]-i[0]+1):
			selection.append(j+i[0])

if sl[0].find(".")!= -1:
	if sl[0].split('.')[1].split('[')[0]=='vtx':
		sel_type = kGeotype.vertex
		m.selectionType = kGeotype.vertex
	if sl[0].split('.')[1].split('[')[0]=='e':
		sel_type = kGeotype.edge
		m.selectionType = kGeotype.edge
		for i in range(0,len(selection)):
			pArray = [0, 0] 
			x = OpenMaya.MScriptUtil() 
			x.createFromList(pArray,2)
			y = x.asInt2Ptr()
			m.meshFn.getEdgeVertices(selection[i],y)
			m.edges.append([x.getInt2ArrayItem( y, 0, 0 ),x.getInt2ArrayItem( y, 0, 1 )])
			selection[i]=i
	if sl[0].split('.')[1].split('[')[0]=='f':
		sel_type = kGeotype.face
		m.selectionType = kGeotype.face

"""
