import random
import math  # degrees,tan,pi,sin,cos,modf
from copy import copy
from time import time

from geometry import (
    BBox,
    EPSILON,
    OBBox,
    Point,
    Polygon,
    Ray,
    Transform,
    Vector,
    fit,
    interpolateBezier,
)
from noise import Noise

import lists
from chull import Hull
from delaunay import Delaunay
from lists import CycleList

VERBOSE = 1
# kLoad = lists.Enumeration("empty|vertices|faces|edges|normals|bbox|pivot")
kGeotype = lists.Enumeration("face|edge|vertex")
kResult = lists.Enumeration("updateVertex|updateMesh|updateSelection")


def printv(*args):
    if VERBOSE >= args[-1]:
        print(args[:-1])


class Mesh(object):
    def __init__(self):
        self.faces = []
        self.vertices = []
        self.normals = []
        # edges used by request, otherwords fill yourself
        self.edges = []
        self.uvs = []
        self.face_uvs = []
        self.pivot = Vector()
        self.bbox = BBox()
        self.selectionType = kGeotype.face
        self.mode = ""

    def __str__(self):
        s = ""
        for i in self.vertices:
            s = s + "," + str(i)
        n = ""
        for i in self.normals:
            n = n + "," + str(i)
        return (
            "face count: "
            + str(len(self.faces))
            + "\nvertex count: "
            + str(len(self.vertices))
            + "\nfaces: "
            + str(self.faces)
            + "\nvertices: "
            + s
            + "\nnormals: "
            + n
        )

    def __call__(self):
        return self

    def backup(self):
        self.backup = self

    def restore(self):
        self.faces = self.backup.faces
        self.vertices = self.backup.vertices
        self.normals = self.backup.normals
        self.edges = self.backup.edges

    """                                        SELECTIONS                                             """

    def findVertexNeighbor(self, vertex, faces):
        neighbors = []
        for face in faces:
            inface_id = lists.find(self.faces[face], vertex)
            if inface_id == 0:
                first = self.faces[face][len(self.faces[face]) - 1]
                last = self.faces[face][1]
            else:
                if inface_id == len(self.faces[face]) - 1:
                    first = self.faces[face][len(self.faces[face]) - 2]
                    last = self.faces[face][0]
                else:
                    first = self.faces[face][inface_id - 1]
                    last = self.faces[face][inface_id + 1]
            if inface_id > -1:
                find = lists.find(neighbors, first)
                if find == -1:
                    neighbors.append(first)
                find = lists.find(neighbors, last)
                if find == -1:
                    neighbors.append(last)
        return neighbors

    def __selectFaceBorders(self, select):
        border_edges = []
        # separate by pairs
        for f in select:
            for i in range(1, len(self.faces[f])):
                border_edges.append([self.faces[f][i - 1], self.faces[f][i]])
            border_edges.append(
                [self.faces[f][len(self.faces[f]) - 1], self.faces[f][0]]
            )
        # print border_edges

        # remove duplicates
        border = []
        for i in range(0, len(border_edges)):
            if not (
                len(lists.duplicates_of(border_edges, border_edges[i])) == 1
                and len(
                    lists.duplicates_of(
                        border_edges, [border_edges[i][1], border_edges[i][0]]
                    )
                )
                == 1
            ):
                border.append(border_edges[i])

        # print border

        # sort 2d
        def srt(k):
            if len(k) < 1:
                return []
            lst = []
            lst.append(k[0])
            m = []
            for i in range(0, len(k)):
                for j in range(0, len(k)):
                    if k[j] not in lst:
                        if lst[len(lst) - 1][1] == k[j][0]:
                            lst.append(k[j])
                            break
            for i in range(0, len(k)):
                if k[i] not in lst:
                    m.append(k[i])
            n = []
            n.append(lst)
            n.extend(srt(m))
            return n

        lst = srt(border)
        # print lst

        # get first element only
        border_vertices = []
        for i in range(0, len(lst)):
            s = []
            for j in range(0, len(lst[i])):
                s.append(lst[i][j][0])
            border_vertices.append(s)
        return border_vertices

    def __selectFaceBordersEx(self, select):
        # border_vertices = self.__selectFaceBorders(select)
        border_edges = []
        # separate by pairs
        for f in select:
            for i in range(1, len(self.faces[f])):
                border_edges.append([self.faces[f][i - 1], self.faces[f][i]])
            border_edges.append(
                [self.faces[f][len(self.faces[f]) - 1], self.faces[f][0]]
            )
        # print border_edges

        # remove duplicates
        border = []
        border_reject = []
        for i in range(0, len(border_edges)):
            if not (
                len(lists.duplicates_of(border_edges, border_edges[i])) == 1
                and len(
                    lists.duplicates_of(
                        border_edges, [border_edges[i][1], border_edges[i][0]]
                    )
                )
                == 1
            ):
                border.append(border_edges[i])
            else:
                border_reject.append(border_edges[i])
        # print border
        # print border_reject

        # sort 2d
        def srt(k):
            if len(k) < 1:
                return []
            lst = []
            lst.append(k[0])
            m = []
            for i in range(0, len(k)):
                for j in range(0, len(k)):
                    if k[j] not in lst:
                        if lst[len(lst) - 1][1] == k[j][0]:
                            lst.append(k[j])
                            break
            for i in range(0, len(k)):
                if k[i] not in lst:
                    m.append(k[i])
            n = []
            n.append(lst)
            n.extend(srt(m))
            return n

        lst = srt(border)
        # print lst

        # get first element only
        border_vertices = []
        for i in range(0, len(lst)):
            s = []
            for j in range(0, len(lst[i])):
                s.append(lst[i][j][0])
            border_vertices.append(s)
        # SLOW get group faces
        border_group_dup = []
        for i in range(0, len(border_vertices)):
            border_group_dup.append([])
            for k in range(0, len(border_vertices[i])):
                for j in select:
                    # print border_vertices[i][k],self.faces[j]
                    if border_vertices[i][k] in self.faces[j]:
                        border_group_dup[len(border_group_dup) - 1].extend([j])
        # remove group duplicates
        border_group = []
        for i in range(0, len(border_group_dup)):
            border_group.append(list(set(border_group_dup[i])))
        return [border_vertices, border_group, border_reject]

    def __selectFacesInterior(self, select):
        all_verts = []
        for f in select:
            for i in range(len(self.faces[f])):
                all_verts.append(self.faces[f][i])
        border = self.__selectFaceBorders(select)
        all_verts = list(set(all_verts))
        return lists.remove_duplicates(all_verts, border[0])

    def __selectEdgesGroups(self, sel_edges):
        sel_pairs = []
        borders = []
        for edge in sel_edges:
            sel_pairs += [self.edges[edge]]
        borders = [sel_pairs[0]]
        sel_pairs = sel_pairs[1:]
        l0 = lists.get_row(sel_pairs, 0)
        l1 = lists.get_row(sel_pairs, 1)
        findy = True
        while findy:
            findy = False
            find = lists.find(l0, borders[-1][0])
            if find > -1:
                borders[-1] = [l1[find]] + borders[-1]
                l0 = l0[:find] + l0[find + 1 :]
                l1 = l1[:find] + l1[find + 1 :]
                findy = True
            find = lists.find(l1, borders[-1][0])
            if find > -1:
                borders[-1] = [l0[find]] + borders[-1]
                l0 = l0[:find] + l0[find + 1 :]
                l1 = l1[:find] + l1[find + 1 :]
                findy = True
            find = lists.find(l1, borders[-1][-1])
            if find > -1:
                borders[-1] = borders[-1] + [l0[find]]
                l0 = l0[:find] + l0[find + 1 :]
                l1 = l1[:find] + l1[find + 1 :]
                findy = True
            find = lists.find(l0, borders[-1][-1])
            if find > -1:
                borders[-1] = borders[-1] + [l1[find]]
                l0 = l0[:find] + l0[find + 1 :]
                l1 = l1[:find] + l1[find + 1 :]
                findy = True
            if not findy and len(l0) > 0:
                borders += [[l0[0], l1[0]]]
                l0 = l0[1:]
                l1 = l1[1:]
                findy = True
        for i in range(len(borders)):
            borders[i] = lists.group_duplicates(borders[i])
        return borders

    def __selectVertexGroups(self, verts):
        # print verts
        cverts = copy(verts)
        vert_groups = [[cverts[0]]]
        passed_verts = [cverts[0]]
        cverts = cverts[1:]
        while len(cverts) > 0:
            neighbors = self.__selectConvertFV(
                self.vertices[cverts[0]].parent_faces
            )
            count = 0
            finds = []
            for neighbor in neighbors:
                if neighbor in passed_verts:
                    for i in range(len(vert_groups)):
                        if (neighbor in vert_groups[i]) and cverts[
                            0
                        ] not in vert_groups[i]:
                            vert_groups[i] += [cverts[0]]
                            count += 1
                            finds += [i]
                    passed_verts += [cverts[0]]
            if count == 0:
                vert_groups += [[cverts[0]]]
                passed_verts += [cverts[0]]
            cverts = cverts[1:]

            # print "vert_groups",vert_groups
            # print "cverts",cverts

            if count > 1:
                finds.sort()
                # print finds
                vert_groups_combine = vert_groups[: finds[0]]
                # print "vert_groups_combine",vert_groups_combine
                for i in range(len(finds) - 1):
                    vert_groups_combine += vert_groups[
                        finds[i] + 1 : finds[i + 1]
                    ]
                vert_groups_combine += vert_groups[finds[-1] + 1 :]
                # print "vert_groups_combine",vert_groups_combine
                vert_groups_combine += [vert_groups[finds[0]]]
                # print "vert_groups_combine",vert_groups_combine
                for i in range(1, len(finds)):
                    vert_groups_combine[-1] += vert_groups[finds[i]]
                vert_groups = vert_groups_combine
                # print "vert_groups",vert_groups

        for i in range(len(vert_groups)):
            vert_groups[i] = lists.group_duplicates(vert_groups[i])
        # print vert_groups
        return vert_groups

    def __selectConvertVF2(self, edges):
        # select face if exact vertex pair in it| in case of empty edges array
        mesh_edges = []
        for i in range(0, len(self.faces)):
            mesh_edges.append([])

            for j in range(0, len(self.faces[i])):
                if j == len(self.faces[i]) - 1:
                    mesh_edges[i].extend([[self.faces[i][j], self.faces[i][0]]])
                    mesh_edges[i].extend([[self.faces[i][0], self.faces[i][j]]])
                else:
                    mesh_edges[i].extend(
                        [[self.faces[i][j], self.faces[i][j + 1]]]
                    )
                    mesh_edges[i].extend(
                        [[self.faces[i][j + 1], self.faces[i][j]]]
                    )
        sel_faces = []
        # print mesh_edges
        for i in range(0, len(self.faces)):
            for edge in edges:
                if edge in mesh_edges[i]:
                    sel_faces.append(i)
        return list(set(sel_faces))

    def __selectConvertEF(self, edges):
        # select if both edge vertices in face
        faces = []
        for edge in edges:
            v1 = self.edges[edge][0]
            v2 = self.edges[edge][1]
            for i in range(0, len(self.faces)):
                if v1 in self.faces[i] and v2 in self.faces[i]:
                    faces.append(i)
        faces = list(set(faces))
        return faces

    def __selectConvertEF1(self, edges):
        # select if one edge vertex in face
        faces = []
        for edge in edges:
            v1 = self.edges[edge][0]
            v2 = self.edges[edge][1]
            for i in range(0, len(self.faces)):
                if v1 in self.faces[i] or v2 in self.faces[i]:
                    faces.append(i)
        faces = list(set(faces))
        return faces

    def __selectConvertFEV(self, faces):
        # face to vertex pairs according to edges
        edge_verts = []
        for face in faces:
            face_verts = self.faces[face]
            for i in range(len(face_verts)):
                if i == len(face_verts) - 1:
                    edge_verts.append([face_verts[i], face_verts[0]])
                else:
                    edge_verts.append([face_verts[i], face_verts[i + 1]])
        return edge_verts

    def __selectConvertFE(self, faces):
        edge_verts = []
        for face in faces:
            face_verts = self.faces[face]
            for i in range(len(face_verts)):
                if i == len(face_verts) - 1:
                    edge_verts.append([face_verts[i], face_verts[0]])
                    edge_verts.append([face_verts[0], face_verts[i]])
                else:
                    edge_verts.append([face_verts[i], face_verts[i + 1]])
                    edge_verts.append([face_verts[i + 1], face_verts[i]])
        edges = []
        for i in range(len(edge_verts)):
            find = lists.find(self.edges, edge_verts[i])
            if find != -1:
                edges.append(find)
        edges = list(set(edges))
        return edges

    def __selectConvertVF(self, vertices):
        faces = []

        for vertex in vertices:
            faces += self.vertices[vertex].parent_faces

        return faces

    def selectGrowF(self, sel_faces):
        verts = self.__selectConvertFV(sel_faces)
        return self.__selectConvertVF(verts)

    def selectGrowE(self, sel_edges):
        verts = self.__selectConvertEV(sel_edges)
        return self.__selectConvertVE(verts)

    def selectGrowV(self, sel_verts):
        new_verts = []
        for vert in sel_verts:
            new_verts += [
                self.findVertexNeighbor(vert, self.vertices[vert].parent_faces)
            ]
        new_verts = lists.group_duplicates(new_verts)
        return new_verts

    def __selectLoopGroupAnchors(self, border):
        anchors = []
        anchor_faces = []
        # print border
        for i in range(len(border)):
            faces = self.__selectConvertVF([border[i]])
            if i == len(border) - 1:
                inc = -1
            else:
                inc = 1
            loop_face_verts = []
            # print
            # print "search vert",border[i]
            # print "next vert",border[i+inc]
            for face in faces:
                if border[i + inc] in self.faces[face]:
                    loop_face_verts += self.faces[face]
            # print border[i],faces
            neighbors = self.findVertexNeighbor(border[i], faces)
            neighbors = lists.leave_duplicates(neighbors, loop_face_verts)
            neighbors = lists.remove_duplicates(neighbors, [border[i + inc]])
            # print i,border[i],neighbors
            if i > 0:
                anchor_faces_old = anchor_faces
            else:
                anchor_faces_old = self.__selectConvertVF([border[i]])
            anchor_faces = self.__selectConvertVF([neighbors[0]])
            # print "anchor_faces",anchor_faces
            # print "anchor_faces_old",anchor_faces_old
            anchor_similar_face = lists.leave_duplicates(
                anchor_faces, anchor_faces_old
            )
            if len(anchor_similar_face) == 0:
                neighbors = neighbors[::-1]
                anchor_faces = self.__selectConvertVF([neighbors[0]])
            # print "anchor_similar_face",anchor_similar_face

            if len(neighbors) == 2:
                anchors += [neighbors]
        return anchors

    def __selectGrowLoopGroup(self, border):
        border_new = copy(border)
        faces = self.__selectConvertVF([border[0]])
        loop_face_verts = []
        for face in faces:
            if border[1] in self.faces[face]:
                loop_face_verts += self.faces[face]
        neighbors = self.findVertexNeighbor(border[0], faces)
        neighbors = lists.remove_duplicates(neighbors, loop_face_verts)
        if len(neighbors) == 1:
            border_new = neighbors + border_new
        faces = self.__selectConvertVF([border[len(border) - 1]])
        loop_face_verts = []
        for face in faces:
            if border[len(border) - 2] in self.faces[face]:
                loop_face_verts += self.faces[face]
        neighbors = self.findVertexNeighbor(border[len(border) - 1], faces)
        neighbors = lists.remove_duplicates(neighbors, loop_face_verts)
        if len(neighbors) == 1:
            border_new += neighbors
        return border_new

    def __selectConvertFV(self, faces):
        vertices = []
        for face in faces:
            vertices.extend(self.faces[face])
        vertices = lists.group_duplicates(vertices)
        return vertices

    def __selectConvertEV(self, edges):
        vertices = []
        for edge in edges:
            vertices.extend(self.edges[edge])
        vertices = lists.group_duplicates(vertices)
        return vertices

    def __selectConvertVE(self, sel_verts):
        sel_edges = []
        for i in range(len(self.edges)):
            if self.edges[i][0] in sel_verts:
                sel_edges += [i]
            elif self.edges[i][1] in sel_verts:
                sel_edges += [i]
        return sel_edges

    def selectConvert(self, selection, fromtype, totype):
        if fromtype == kGeotype.face:
            if totype == kGeotype.edge:
                return self.__selectConvertFE(selection)
            elif totype == kGeotype.vertex:
                return self.__selectConvertFV(selection)
        if fromtype == kGeotype.edge:
            if totype == kGeotype.face:
                return self.__selectConvertEF1(selection)
            elif totype == kGeotype.vertex:
                return self.__selectConvertEV(selection)
        if fromtype == kGeotype.vertex:
            if totype == kGeotype.face:
                return self.__selectConvertVF(selection)
            elif totype == kGeotype.edge:
                return self.__selectConvertVE(selection)

    def selectSymmetry(self):
        pass

    def selectSimilarF(self, sel_face):
        def sort_by_len(a, b):
            if a[1] > b[1]:
                return 1
            elif a[1] == b[1]:
                return 0
            else:
                return -1

        faces_length = []
        for i in range(len(self.faces)):
            faces_length.append([i, len(self.faces[i])])
        faces_length.sort(sort_by_len)
        faces_groups = [[0, 0]]
        faces_counts = [faces_length[0][1]]
        sorted_faces = [faces_length[0][0]]
        for i in range(1, len(self.faces)):
            sorted_faces += [faces_length[i][0]]
            if faces_length[i][1] == faces_length[i - 1][1]:
                faces_groups[len(faces_groups) - 1][1] = i
            else:
                faces_groups += [[i, i]]
                faces_counts += [faces_length[i][1]]
        find = lists.find(faces_counts, len(self.faces[sel_face[0]]))
        if find > -1:
            return sorted_faces[
                faces_groups[find][0] : faces_groups[find][1] + 1
            ]
        else:
            return 0

    def selectFByAngle(self, sel_faces, angle=0.0):
        grow_faces = copy(sel_faces)
        for face in grow_faces:
            grows = self.selectGrowF([face])
            for grow in grows:
                if (
                    grow not in grow_faces
                    and math.degrees(
                        self.getNormal(face).angle(self.getNormal(grow))
                    )
                    <= angle
                ):
                    grow_faces += [grow]
        return grow_faces

    def selectFByNormal(self, sel_faces, delta=0.05):
        def sort_normals(a, b):
            if a[0].x < b[0].x:
                return -1
            elif a[0].x > b[0].x:
                return 1
            else:
                if a[0].y < b[0].y:
                    return -1
                elif a[0].y > b[0].y:
                    return 1
                else:
                    if a[0].z < b[0].z:
                        return -1
                    elif a[0].z > b[0].z:
                        return 1
                    else:
                        return 0

        def find_normal(sorted_normals, normal, delta):
            start = -1
            end = -1

            for i in range(1, len(sorted_normals)):
                if start == -1:
                    if (
                        sorted_normals[i - 1][0].x - delta <= normal.x
                        and normal.x <= sorted_normals[i][0].x + delta
                    ):
                        if (
                            sorted_normals[i - 1][0].y - delta <= normal.y
                            and normal.y <= sorted_normals[i][0].y + delta
                        ):
                            if (
                                sorted_normals[i - 1][0].z - delta <= normal.z
                                and normal.z <= sorted_normals[i][0].z + delta
                            ):
                                start = i - 1
                elif (
                    sorted_normals[i][0].x + delta < normal.x
                    or sorted_normals[i][0].y + delta < normal.y
                    or sorted_normals[i][0].z + delta < normal.z
                ):
                    end = i
                    break
            return [start, end]

        new_sel_faces = []
        if len(self.normals) < 1:
            self.recomputeNormals()
        sorted_normals = []
        for i in range(len(self.faces)):
            sorted_normals.append([self.normals[i], i])
        sorted_normals.sort(sort_normals)
        # for i in range(len(self.faces)):
        # print(i,sorted_normals[i][0],sorted_normals[i][1])
        for face in sel_faces:
            normal = self.normals[face]
            find = find_normal(sorted_normals, normal, delta)
            for i in range(find[0], find[1]):
                new_sel_faces.append(sorted_normals[i][1])

        # new_sel_faces += sel_faces
        new_sel_faces = lists.group_duplicates(new_sel_faces)
        # print new_sel_faces
        return new_sel_faces

    """                                        MISCELLANEOUS                                          """

    def recomputeNormals(self):
        for face in range(len(self.faces)):
            self.normals.append(self.__computeFaceNormal(face))

    def __spherifyPoint(self, center, radius, vert, factor):
        vert1 = vert - center
        vert1.normalize()
        t = radius / (
            (vert1.x * vert1.x + vert1.y * vert1.y + vert1.z * vert1.z) ** 0.5
        )
        new_vert = vert1 * t + center
        return vert.lerp(new_vert, factor)

    def __computeFaceNormal(self, face):
        normal = Vector()
        for i in range(len(self.faces[face])):
            v1 = self.vertices[self.faces[face][i]]
            if i == len(self.faces[face]) - 1:
                v2 = self.vertices[self.faces[face][0]]
            else:
                v2 = self.vertices[self.faces[face][i + 1]]
            normal = normal + v1.cross(v2)
        normal = normal.normalize()
        return normal

    def __computeVertexNormal(self, vert, faces=None):
        if not faces:
            neighbors = self.findVertexNeighbor(
                vert, self.vertices[vert].parent_faces
            )
        else:
            neighbors = self.findVertexNeighbor(vert, faces)
        normal = Vector()
        for i in range(len(neighbors) - 1):
            normal += (self.vertices[neighbors[i]] - self.vertices[vert]).cross(
                self.vertices[neighbors[i + 1]] - self.vertices[vert]
            )
        normal = normal.normalize()
        return normal

    def __faceCenter(self, face):
        center = Point()
        for i in range(0, len(self.faces[face])):
            center = center + self.vertices[self.faces[face][i]]
        center = center / len(self.faces[face])
        return center

    def __sortVerticesCCW(self, sel_verts):
        center = Point()
        # print sel_verts
        new_verts = []
        vert_angles = []
        for i in range(len(sel_verts)):
            center += self.vertices[sel_verts[i]]
            vert_angles.append([sel_verts[i]])
        center = center / len(sel_verts)

        v1 = self.vertices[sel_verts[0]]
        v2 = self.vertices[sel_verts[1]]
        v3 = self.vertices[sel_verts[2]]
        (v2 - v1).cross(v3 - v1)
        t1 = Transform()
        t2 = Transform()
        t1.translate(-center)
        t2.from2Vectors((v2 - v1).normalize(), (v1 - v3).normalize())

        for i in range(0, len(sel_verts)):
            face_vert = t1.applyTransform(self.vertices[sel_verts[i]])
            face_vert = t2.applyTransform(face_vert)
            vert_angles[i].extend([face_vert])
            # wself.vertices[sel_verts[i]]=face_vert

        # print vert_angles
        def clockwise_sort(a, b):
            if a[1].x >= 0 and b[1].x < 0:
                return -1
            if a[1].x == 0.0 and b[1].x == 0:
                return a[1].z <= b[1].z
            det = a[1].x * b[1].z - b[1].x * a[1].z
            if det == 0.0:
                return 0
            elif det > 0:
                return 1
            else:
                return -1

        vert_angles.sort(clockwise_sort)
        for i in range(len(sel_verts)):
            new_verts.append(vert_angles[i][0])
        # print new_verts
        # self.faces[0]=new_verts
        return new_verts

    def __deleteVertices(self, verts):

        verts.sort()
        # next should be uncommented if you want to continue modelling
        # self.rebuildVertP()

        swap = []
        verts_swap = copy(verts)
        i = 0
        while len(verts_swap) > 0:  # and i<100:
            if len(self.vertices) - i - 1 not in verts:
                if verts_swap[0] < len(self.vertices) - len(verts):
                    swap += [len(self.vertices) - i - 1]
                    verts_swap = verts_swap[1:]
                else:
                    verts_swap = verts_swap[1:]
            i += 1
        # print swap
        # swap.sort()

        start_time = time()
        for k in range(len(swap)):
            self.vertices[verts[k]] = self.vertices[swap[k]]
            faces_involved = self.__selectConvertVF([swap[k]])
            for face in faces_involved:
                find = lists.find(self.faces[face], swap[k])
                # uvs should be handled here
                self.faces[face][find] = verts[k]

        start_time = time() - start_time
        printv(str(start_time) + " __deleteVertices faces update Elapsed", 2)

        self.vertices = self.vertices[: len(self.vertices) - len(verts)]

    def __deleteNormals(self, faces):
        start_time = time()
        # faces.sort()

        new_normals = self.normals[: faces[0]]
        for i in range(len(faces) - 1):
            new_normals += self.normals[faces[i] + 1 : faces[i + 1]]
        new_normals += self.normals[faces[len(faces) - 1] + 1 :]
        self.normals = new_normals

        start_time = time() - start_time
        print(str(start_time) + " __deleteNormals Elapsed")

    def __deleteFaces(self, faces):
        if len(faces) > 0:
            start_time = time()
            faces.sort()
            new_faces = copy(self.faces[: faces[0]])
            for i in range(len(faces) - 1):
                new_faces += self.faces[faces[i] + 1 : faces[i + 1]]
            new_faces += self.faces[faces[-1] + 1 :]
            self.faces = new_faces
            start_time = time() - start_time
            print(str(start_time) + " __deleteFaces Elapsed")

            self.__deleteNormals(faces)

    def getNormal(self, face):
        return self.normals[face]

    def addVertex(self, value):
        self.vertices += [value]

    def getVertex(self, id):
        return self.vertices[id]

    def updateVertex(self, id, value):
        p = self.vertices[id].parent_faces
        self.vertices[id] = value  # copy(value)
        self.vertices[id].parent_faces = p

    def addFace(self, value):
        # uvs should be handled here
        self.faces.append(value)
        self.normals.append(self.__computeFaceNormal(len(self.faces) - 1))
        for i in value:
            self.vertices[i].parent_faces += [len(self.faces) - 1]

    def updateFace(self, id, value):
        # uvs should be handled here
        for vert in self.faces[id]:
            self.vertices[vert].parent_faces = lists.remove_valuez(
                self.vertices[vert].parent_faces, id
            )
        self.faces[id] = copy(value)
        self.normals[id] = self.__computeFaceNormal(id)
        for vert in self.faces[id]:
            self.vertices[vert].parent_faces += [id]

    def addFaces(self, lst):
        for i in lst:
            self.addFace(i)

    def __updateFaceVert(self, id, find_id, repl_id):
        self.updateFace(
            id,
            self.faces[id][:find_id]
            + [repl_id]
            + self.faces[id][find_id + 1 :],
        )

    def rebuildVertP(self):
        # add face links to vertices
        start_time = time()

        for i in range(len(self.vertices)):
            self.vertices[i].parent_faces = []
        for i in range(len(self.faces)):
            for vert in self.faces[i]:
                self.vertices[vert].parent_faces += [i]
        start_time = time() - start_time
        print(str(start_time) + " rebuildVertP Elapsed")

    def __connectFace(self, sel_face, first, second, connections):
        # first and second are ids | corner not implemented
        face_cycle = CycleList(self.faces[sel_face])
        new_faces = []
        # print face_cycle
        # print "first,second ",first,second
        for i in range(1, connections):
            first_con = first + i
            second_con = second - i
            # print face_cycle[first_con],face_cycle[first_con+1],face_cycle[second_con-1],face_cycle[second_con]
            new_faces.append(
                [
                    face_cycle[second_con],
                    face_cycle[second_con + 1],
                    face_cycle[first_con - 1],
                    face_cycle[first_con],
                ]
            )
        new_faces += [
            (
                face_cycle[first + connections - 1 : second - connections + 2]
            ).list
        ]
        new_faces += [face_cycle.list[second:] + [face_cycle.list[0]]]
        # print new_faces
        return new_faces

    """                                        OPERATIONS                                             """
    # insertCylinder spherify capParallel extrude relax capCylinder connectVertices connectEdges relax triangulate
    # makePlanar collapseEdges collapseVertices splitEdges pushVertices dissolve faceNgon spaceLoops centerLoops
    # generateConvexHull clipPlane radialSymmetry symmetry noise detach slideLoop flowLoop gridTasselate
    # straightLoop
    # selectFByAngle selectSimilarF selectFByNormal
    # Total: 29 mesh operations, 3 select operations
    # WIPquadChamfer
    """
    
    weld borders
    corner align (like building corner)
    break to elements?
    spline from edges

    curveLoop
    remove loop/ring
    distance auto ring connect
    spline to mesh

    mirror/delete mirror
    select symmetry
    test symmetry
    
    save selections
    pivot to face,edge,vertex
    move with keys
    place highlight

    space tool
    interactive array
    distribute objects
    align object to face normal

    fairing
    hinge
    conform mesh

    bake ao,cavity,hard edges to vertex color?
    fracture
    
    delaunay
    __update = update private copy method
    """

    def test(self):
        o = OBBox()
        o.fromPointSet(self.vertices)
        t = Transform()
        t.scaleLocal(0.1, Vector(), o.vectors[0])
        for v in range(len(self.vertices)):
            self.updateVertex(v, t.applyTransform(self.vertices[v]))
        for v in o.vectors:
            self.addVertex(v)

    def multiDuplicateTransform(self, mesh, matrix, **kwargs):
        new_vertices = []
        old_vcount = len(self.vertices)
        for i in range(len(mesh.vertices)):
            new_vertices += [mesh.vertices[i].applyTransform(matrix)]
        self.vertices += new_vertices
        do_faces = kwargs.get("faces", 1)
        if do_faces:
            new_faces = []
            for i in range(len(mesh.faces)):
                new_faces += [[]]
                for j in range(len(mesh.faces[i])):
                    new_faces[-1] += [mesh.faces[i][j] + old_vcount]
            self.faces += new_faces

    def gridTasselate(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        step_size = kwargs.get("step_size", 1)

        if selection_type != kGeotype.face:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.face
            )

        # self.bbox = [Point(min.x,min.y,min.z),Point(max.x,max.y,max.z),Point(center.x,center.y,center.z)]
        if self.bbox is None:
            return
        xsteps = int((self.bbox[1].x - self.bbox[0].x) / step_size) + 1
        ysteps = int((self.bbox[1].y - self.bbox[0].y) / step_size) + 1
        zsteps = int((self.bbox[1].z - self.bbox[0].z) / step_size) + 1
        printv("xyzsteps", xsteps, ysteps, zsteps, 3)
        for i in range(xsteps):
            self.clipPlane(
                False,
                Ray(
                    Vector(self.bbox[0].x + step_size * i, 0, 0),
                    Vector(1, 0, 0),
                ),
            )
        for i in range(ysteps):
            self.clipPlane(
                False,
                Ray(
                    Vector(0, self.bbox[0].y + step_size * i, 0),
                    Vector(0, 1, 0),
                ),
            )
        for i in range(zsteps):
            self.clipPlane(
                False,
                Ray(
                    Vector(0, 0, self.bbox[0].z + step_size * i),
                    Vector(0, 0, 1),
                ),
            )
        return [kResult.updateMesh]

    def delaunay(self):
        def addSphere(c, r):
            self.addVertex(c)

            for i in range(30):
                ze = random.uniform(-r, r)
                phi = random.uniform(0, 2 * math.pi)
                # in sphere volume
                # theta = 1/math.sin(ze/r)
                theta = math.asin(ze / r)
                x = r * math.cos(theta) * math.cos(phi) + c.x
                y = r * math.cos(theta) * math.sin(phi) + c.y
                z = ze + c.z
                self.addVertex(Point(x, y, z))

        # d = Delaunay()
        verts = []
        min, max = -10, 10
        for i in range(20):
            random.seed(i)

            verts += [
                Point(
                    fit(random.random(), 0, 1, min, max),
                    fit(random.random(), 0, 1, min, max),
                    fit(random.random(), 0, 1, min, max),
                )
            ]
        verts += [Point()]
        d = Delaunay(verts, max)
        # for v in d.vertices:
        #    self.addVertex(v)
        # self.addFace(lists.enumerate_list(self.vertices))
        # for tetra in d.tetras:
        self.addVertex(d.tetras[0][0])
        self.addVertex(d.tetras[0][1])
        self.addVertex(d.tetras[0][2])
        self.addVertex(d.tetras[0][3])
        self.addVertex(d.tetras[0].center)
        # addSphere(d.tetras[0].circumcenter,d.tetras[0].circumradius)
        self.addFace(lists.enumerate_list(self.vertices))

        print(self)

    def detach(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        if selection_type != kGeotype.face:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.face
            )

        new_verts = []
        old_verts = []
        new_faces = []
        for f in selection:
            new_faces += [self.faces[f]]
            old_verts += self.faces[f]
        old_verts = lists.group_duplicates(old_verts)
        for i in range(len(new_faces)):
            for j in range(len(new_faces[i])):
                new_faces[i][j] = lists.find(old_verts, new_faces[i][j])
        for i in range(len(old_verts)):
            new_verts += [self.vertices[old_verts[i]]]
        self.vertices = new_verts
        self.faces = new_faces
        return [kResult.updateMesh]

    def radialSymmetry(self, copies):
        # set attributes not implemented yet
        angle = math.pi / float(copies)
        self.clipPlane(True, Ray(Vector(0, 0, 0), Vector(0, 0, -1)))
        self.rebuildVertP()
        self.clipPlane(
            True, Ray(Vector(0, 0, 0), Vector(0, 1, 1 / math.tan(angle)))
        )

        new_vertices = copy(self.vertices)

        t = Transform()
        t.scale(Vector(1, 1, -1))
        old_vcount = len(self.vertices)
        for i in range(old_vcount):
            new_vertices[i] = t.applyTransform(new_vertices[i])

        self.vertices += new_vertices
        new_faces = copy(self.faces)

        for i in range(len(new_faces)):
            new_faces[i] = new_faces[i][::-1]
            for j in range(len(new_faces[i])):
                new_faces[i][j] += old_vcount
        self.faces += new_faces

        sym_vertices = copy(self.vertices)
        sym_faces = copy(self.faces)
        t_rotate = Transform()

        for i in range(copies - 1):
            t_rotate.rotateAxis(angle * 2 * (i + 1), Vector(1, 0, 0))

            new_vertices = copy(sym_vertices)
            old_vcount = len(self.vertices)
            for i in range(len(sym_vertices)):
                new_vertices[i] = t_rotate.applyTransform(new_vertices[i])

            self.vertices += new_vertices
            new_faces = copy(sym_faces)

            for i in range(len(new_faces)):
                new_faces[i] = new_faces[i][::1]
                for j in range(len(new_faces[i])):
                    new_faces[i][j] += old_vcount
            self.faces += new_faces
        return [kResult.updateMesh]

    def symmetry(self):
        # set attributes not implemented yet
        self.clipPlane(True, Ray(Vector(0, 0, 0), Vector(0, 0, -1)))

        new_vertices = copy(self.vertices)

        t = Transform()
        t.scale(Vector(1, 1, -1))
        old_vcount = len(self.vertices)
        for i in range(old_vcount):
            new_vertices[i] = t.applyTransform(new_vertices[i])

        self.vertices += new_vertices
        new_faces = copy(self.faces)

        for i in range(len(new_faces)):
            new_faces[i] = new_faces[i][::-1]
            for j in range(len(new_faces[i])):
                new_faces[i][j] += old_vcount
        self.faces += new_faces
        return [kResult.updateMesh]

    def clipPlane(
        self, delete_remains=True, ray=Ray(Vector(0, 0, 0), Vector(0, 1, 0))
    ):
        verts_rejected = []
        verts_sides = []
        for i in range(len(self.vertices)):
            ray_test = ray.pointPlaneSide(self.vertices[i])
            verts_sides.append(ray_test)
            if not ray_test:
                verts_rejected += [i]

        faces_involved = []
        faces_rejected = []

        start_time = time()
        for i in range(0, len(self.faces)):
            intersect = 0
            for j in range(len(self.faces[i])):
                intersect += verts_sides[self.faces[i][j]]
            if intersect == 0:
                faces_rejected += [i]
            elif intersect < len(self.faces[i]):
                faces_involved.append(i)

        start_time = time() - start_time
        printv(start_time, "point side test Elapsed", 2)
        # print "faces_rejected ",faces_rejected
        # print "faces_involved ",faces_involved
        start_time = time()

        computed_edges = []
        computed_points = []
        faces_points = []
        # compute intersect points
        for j in range(len(faces_involved)):
            cycle_face = CycleList(self.faces[faces_involved[j]])
            faces_points.append([])
            # computed_edges.append([])
            for i in range(len(cycle_face)):
                if (
                    verts_sides[cycle_face[i]] + verts_sides[cycle_face[i + 1]]
                    == 1
                ):
                    find = lists.find(
                        computed_edges, [cycle_face[i], cycle_face[i + 1]]
                    )
                    if find == -1:
                        we = ray.segmentPlaneHit(
                            [
                                self.vertices[cycle_face[i]],
                                self.vertices[cycle_face[i + 1]],
                            ]
                        )
                        if we != 0:
                            # computed_edges[j].extend([[cycle_face[i], cycle_face[i+1]],[cycle_face[i+1], cycle_face[i]]])
                            computed_edges += [
                                [cycle_face[i], cycle_face[i + 1]],
                                [cycle_face[i + 1], cycle_face[i]],
                            ]
                            self.addVertex(Point(we.x, we.y, we.z))
                            faces_points[j].extend([len(self.vertices) - 1])
                            computed_points += [len(self.vertices) - 1]
                    else:
                        faces_points[len(faces_points) - 1].extend(
                            [computed_points[int(find / 2)]]
                        )

        # print "face_points",faces_points
        # print "computed_edges",computed_edges
        # print "verts_sides ",verts_sides
        # print "computed_points",computed_points
        start_time = time() - start_time
        printv(start_time, "intersection Elapsed", 2)

        def sort_by1(a, b):
            if a[1] > b[1]:
                return 1
            elif a[1] == b[1]:
                return 0
            else:
                return -1

        def build_poly(lst):
            ll = []
            lst2 = [x for x in lst if x]
            if not lst2:
                return [], []
            r = lst2[0]
            for n in lst2[1:]:
                q = [x for x in r if x in n]
                if q:
                    r.extend(n)
                else:
                    ll.append(n)
            return ll, r

        # self.addFace(computed_points)

        start_time = time()
        for facenum in range(len(faces_involved)):
            # sort new vertices by signed length
            sorted_verts = []
            if len(faces_points[facenum]) > 2:
                x = self.vertices[faces_points[facenum][0]]
                y = self.vertices[faces_points[facenum][1]]
                xy = (x - y).length()
                sorted_verts += [[faces_points[facenum][0], 0.0]]
                sorted_verts += [[faces_points[facenum][1], xy]]
                for j in range(2, len(faces_points[facenum])):
                    z = self.vertices[faces_points[facenum][j]]
                    xz = (x - z).length()
                    yz = (y - z).length()
                    if xz > yz or yz < xy:
                        sorted_verts += [[faces_points[facenum][j], xz]]
                    else:
                        sorted_verts += [[faces_points[facenum][j], -xz]]
                sorted_verts.sort(sort_by1)
                sorted_verts = lists.get_row(sorted_verts, 0)
                if verts_sides[self.faces[faces_involved[facenum]][0]]:
                    sorted_verts = sorted_verts[::-1]

                pair_sorted_verts = lists.to_pairs(sorted_verts)
            else:
                sorted_verts = faces_points[facenum]
                if not verts_sides[self.faces[faces_involved[facenum]][0]]:
                    sorted_verts = sorted_verts[::-1]
                pair_sorted_verts = [sorted_verts]

            # print "face",faces_involved[facenum]
            # print "face=",self.faces[faces_involved[facenum]]
            # print "sorted_verts",sorted_verts
            # print "pair_sorted_verts",pair_sorted_verts
            edges = self.__selectConvertFEV([faces_involved[facenum]])
            edges_bottom = copy(edges)
            # print "old_edges",edges
            for j in range(len(edges)):
                if (
                    not verts_sides[edges[j][0]]
                    and not verts_sides[edges[j][1]]
                ):
                    edges[j] = []
                else:
                    find = lists.find(computed_edges, edges[j]) / 2
                    if find > -1:
                        findy = (
                            lists.find(sorted_verts, computed_points[find]) / 2
                        )
                        if verts_sides[edges[j][0]]:
                            edges[j] = [edges[j][0]] + pair_sorted_verts[findy]
                        else:
                            edges[j] = pair_sorted_verts[findy] + [edges[j][1]]
            if not delete_remains:
                for j in range(len(edges_bottom)):
                    if (
                        verts_sides[edges_bottom[j][0]]
                        and verts_sides[edges_bottom[j][1]]
                    ):
                        edges_bottom[j] = []
                    else:
                        find = lists.find(computed_edges, edges_bottom[j]) / 2
                        if find > -1:
                            findy = (
                                lists.find(sorted_verts, computed_points[find])
                                / 2
                            )
                            if not verts_sides[edges_bottom[j][0]]:
                                edges_bottom[j] = [
                                    edges_bottom[j][0]
                                ] + pair_sorted_verts[findy][::-1]
                            else:
                                edges_bottom[j] = pair_sorted_verts[findy][
                                    ::-1
                                ] + [edges_bottom[j][1]]
            # print "new edges",edges
            # print "bottom edges",edges_bottom
            ret = []
            while edges:
                edges, g = build_poly(edges)
                ret.append(g)
            for i in range(len(ret)):
                ret[i] = lists.group_duplicates(ret[i])
            # print "new faces",ret
            self.updateFace(faces_involved[facenum], ret[0])
            self.addFaces(ret[1:])

            if not delete_remains:
                ret = []
                while edges_bottom:
                    edges_bottom, g = build_poly(edges_bottom)
                    ret.append(g)
                for i in range(len(ret)):
                    ret[i] = lists.group_duplicates(ret[i])
                # print "new faces",ret
                # self.updateFace(faces_involved[facenum],ret[0])
                self.addFaces([ret[0]])
                self.addFaces(ret[1:])

        start_time = time() - start_time
        printv(start_time, "build new faces Elapsed", 2)
        # print("faces_rejected",faces_rejected,len(faces_rejected))
        # print("verts_rejected",verts_rejected,len(verts_rejected))
        if delete_remains:
            self.__deleteVertices(verts_rejected)
            self.__deleteFaces(faces_rejected)
        return [kResult.updateMesh]

    def generateConvexHull(self, num_verts, vert_count):
        vert_ids = []
        verts = []
        for i in range(num_verts):
            vert_ids += [int(random() * vert_count)]
        vert_ids = list(set(vert_ids))
        for i in range(len(vert_ids)):
            verts += [self.getVertex(vert_ids[i])]
        hull = Hull(verts)
        export_hull = hull.exportHull()
        self.vertices = export_hull[1]
        self.faces = export_hull[0]
        return [kResult.updateMesh]

    def triangulate(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        if selection_type != kGeotype.face:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.face
            )
        for face in selection:
            poly_verts = []
            for i in range(len(self.faces[face])):
                poly_verts.append(self.vertices[self.faces[face][i]])
            poly = Polygon(
                self.vertices, self.faces[face], self.getNormal(face)
            )
            triPlainIndices = poly.triangulate()
            triIndices = []
            for i in range(len(triPlainIndices) / 3):
                triIndices += [
                    [
                        triPlainIndices[i * 3],
                        triPlainIndices[i * 3 + 1],
                        triPlainIndices[i * 3 + 2],
                    ]
                ]
            self.addFaces(triIndices)
        self.__deleteFaces(selection)
        return [kResult.updateMesh]

    def makeNgon(self, selection, **kwargs):
        # TODO detect quad faces and apply autoorientation
        selection_type = kwargs.get("selection_type", self.selectionType)
        cycle = kwargs.get("cycle", 0)
        if selection_type != kGeotype.vertex:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.vertex
            )

        groups = self.__selectVertexGroups(selection)
        for group in groups:
            center = Vector()
            normal = Vector()
            radius = 0
            for vert in group:
                center += self.vertices[vert]
                normal += self.__computeVertexNormal(vert)
            sides = len(group)

            center /= sides
            normal /= sides
            self.addVertex(center)
            self.addVertex(center + normal)

            normal = normal.normalize()
            axis = Vector(0, -51, 0)
            normalcross = normal.cross(axis).normalize()
            if normalcross.length() == 0:
                axis = Vector(1, 0, 0)
                normalcross = normal.cross(axis).normalize()

            for vert in group:
                mid = center - self.vertices[vert]
                radius += mid.length()

            radius /= sides
            t = Transform()
            t.lookAt(center, center - normal, normalcross)
            for i in range(sides):
                p = Point(
                    math.sin(2 * math.pi / sides * (i + cycle + 1)) * radius,
                    math.cos(2 * math.pi / sides * (i + cycle + 1)) * radius,
                    0,
                )

                p = t.applyTransform(p)

                self.updateVertex(group[i], p)
        return [kResult.updateVertex]

    def makePlanar(self, selection, **kwargs):
        # TODO group detect
        selection_type = kwargs.get("selection_type", self.selectionType)
        if selection_type != kGeotype.face:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.face
            )
        avg_normal = kwargs.get("normal", 0)
        avg_center = Vector()
        if avg_normal.__class__.__name__ != "Vector":
            avg_normal = Vector()
            for face in selection:
                avg_normal += self.getNormal(face)
                avg_center += self.__faceCenter(face)
            avg_normal = (avg_normal / len(selection)).normalize()
        else:
            for face in selection:
                avg_center += self.__faceCenter(face)
        avg_center /= len(selection)
        verts = self.__selectConvertFV(selection)
        plane = Ray(avg_center, avg_normal)
        for vert in verts:
            self.updateVertex(
                vert,
                plane.segmentPlaneHit(
                    [self.vertices[vert], self.vertices[vert] + avg_normal]
                ),
            )
        return [kResult.updateVertex]

    def dissolve(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        if selection_type != kGeotype.face:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.face
            )
        all_verts = self.__selectConvertFV(selection)
        border_faces = self.__selectFaceBorders(selection)
        border_verts = []
        for i in range(len(border_faces)):
            border_verts += border_faces[i]
        interior_verts = lists.remove_duplicates(all_verts, border_verts)
        self.addFaces(border_faces)
        self.__deleteVertices(interior_verts)
        self.__deleteFaces(selection)
        return [kResult.updateMesh]

    def noise(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        amount = kwargs.get("amount", 0.5)
        if selection_type != kGeotype.vertex:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.vertex
            )

        start_time = time()
        for vert in selection:
            n = Noise()
            # v = n.snoise(self.vertices[vert])
            # self.pushVertices([vert],v*amount)
            # v = n.vsnoise(self.vertices[vert])
            # self.updateVertex(vert,self.vertices[vert]+Point(v)*amount)
            # fBm(x,y,z,octaves,lacunarity,gain)
            # v = n.fBm(self.vertices[vert].x,self.vertices[vert].y,self.vertices[vert].z,2,0.3,1)
            # self.pushVertices([vert],v*amount)
            v = n.turbulence(
                self.vertices[vert].x,
                self.vertices[vert].y,
                self.vertices[vert].z,
                2,
                1.2,
                amount,
            )
            # v = n.fBm(self.vertices[vert].x,self.vertices[vert].y,self.vertices[vert].z,8.2,1.2,amount)
            self.updateVertex(
                vert,
                Point(
                    self.vertices[vert].x,
                    self.vertices[vert].y + v,
                    self.vertices[vert].z,
                ),
            )
        start_time = time() - start_time
        print(str(start_time) + " noise Elapsed")
        return [kResult.updateVertex]

    def push(self, selection, **kwargs):
        # TODO impement shrink faces for push
        selection_type = kwargs.get("selection_type", self.selectionType)
        push_amount = kwargs.get("push_amount", 1)

        if selection_type != kGeotype.vertex:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.vertex
            )

        Vector()
        Vector()
        for vert in selection:
            normal = Vector()
            faces_involved = self.__selectConvertVF([vert])
            angle = 0
            faces_normal = []
            for face in faces_involved:
                faces_normal.append(self.getNormal(face))
                normal += faces_normal[len(faces_normal) - 1]
            normal = normal.normalize()
            for i in range(len(faces_involved)):
                angle = max(angle, normal.angle(faces_normal[i]))
            if angle < EPSILON or EPSILON < angle:
                self.vertices[vert].addRuler(
                    normal * push_amount / math.cos(angle)
                )
            else:
                self.vertices[vert].addRuler(normal * push_amount)
        for vert in selection:
            self.updateVertex(
                vert, self.vertices[vert] + self.vertices[vert].ruler
            )
        return [kResult.updateVertex]

    def relax(self, selection, **kwargs):
        # Laplacian smoothing
        selection_type = kwargs.get("selection_type", self.selectionType)
        factor = kwargs.get("factor", 1)
        iterations = kwargs.get("iterations", 1)
        if selection_type != kGeotype.vertex:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.vertex
            )

        neighbor_list = []
        for v in selection:
            vertex_faces = self.__selectConvertVF([v])
            neighbor_list += [self.findVertexNeighbor(v, vertex_faces)]
        for iteration in range(iterations):
            for v in range(len(selection)):
                newPos = Point()
                for i in neighbor_list[v]:
                    newPos += self.vertices[i]
                newPos = newPos / len(neighbor_list[v])
                self.updateVertex(
                    selection[v],
                    self.vertices[selection[v]].lerp(newPos, factor),
                )
                # Additive smoothing
                # inverse = 1/float(iterations+len(self.vertices[v].neighbor)*factor)
                # newPos=(newPos+Vector(factor,factor,factor))*inverse
        return [kResult.updateVertex]

    def spherify(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        factor = kwargs.get("factor", 1)

        if selection_type != kGeotype.vertex:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.vertex
            )

        if "center" in kwargs:
            center = kwargs.get("center")
        else:
            center = Point()
            for i in range(0, len(selection)):
                center = center + self.vertices[selection[i]]
            center = center / len(selection)
        if "radius" in kwargs:
            radius = kwargs.get("radius")
        else:
            radius = 0
            v1 = Vector()
            for i in range(0, len(selection)):
                v1.fromPoints(self.vertices[selection[i]], center)
                radius += v1.length()
            radius = radius / len(selection)
        for sel_vert in selection:
            self.updateVertex(
                sel_vert,
                self.__spherifyPoint(
                    center, radius, self.vertices[sel_vert], factor
                ),
            )
        return [kResult.updateVertex]

    def collapse(self, selection, **kwargs):
        # TODO edges and faces groups
        selection_type = kwargs.get("selection_type", self.selectionType)
        group = kwargs.get("group", 0)
        if selection_type != kGeotype.vertex:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.vertex
            )
        if group:
            groups = self.__selectVertexGroups(selection)
        else:
            groups = [selection]
        delete_faces = []
        delete_verts = []
        delete_verts += selection
        for group in groups:
            center = Point()
            for vert in group:
                center += self.vertices[vert]
            center /= len(group)
            self.addVertex(center)
            new_id = len(self.vertices) - 1
            faces = self.__selectConvertVF(group)
            for face in faces:
                for vert in group:
                    find = lists.find(self.faces[face], vert)
                    if find > -1:
                        self.__updateFaceVert(face, find, new_id)
                self.updateFace(face, lists.group_duplicates(self.faces[face]))
                if len(self.faces[face]) < 3:
                    delete_faces += [face]

        delete_verts = lists.group_duplicates(delete_verts)
        self.__deleteVertices(delete_verts)
        if len(delete_faces) > 0:
            delete_faces = lists.group_duplicates(delete_faces)
            self.__deleteFaces(delete_faces)
        return [kResult.updateMesh]

    def connectVertices(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        if selection_type != kGeotype.vertex:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.vertex
            )
        for vert in selection:
            faces = self.__selectConvertVF([vert])
            for face in faces:
                face_verts = self.__selectConvertFV([face])
                face_verts.pop(lists.find(face_verts, vert))
                for face_vert in face_verts:
                    connect_vert = lists.find(selection, face_vert)
                    if connect_vert != -1:
                        neighbors = self.findVertexNeighbor(
                            selection[connect_vert], [face]
                        )
                        if vert not in neighbors:
                            id1 = lists.find(self.faces[face], vert)
                            id2 = lists.find(
                                self.faces[face], selection[connect_vert]
                            )
                            if id1 > id2:
                                id1, id2 = id2, id1
                            face1 = (
                                self.faces[face][id2:]
                                + self.faces[face][0 : id1 + 1]
                            )
                            face2 = self.faces[face][id1 : id2 + 1]
                            self.updateFace(face, face1)
                            self.addFace(face2)

                            # print "find connect",min(vert,selection[connect_vert])," ",max(vert,selection[connect_vert])," face ",face
        return [kResult.updateMesh]

    def recursiveFillCorner(
        self,
        mid,
        corner,
        outer_points,
        divisions,
        start_divisions,
        center,
        new_faces,
        depth=1,
    ):
        inner_points = []
        corner_sides = len(corner)
        half_start_divisions = (
            math.modf(start_divisions / 2.0)[1]
            + 2 * math.modf(start_divisions / 2.0)[0]
        )
        half_divisions = (
            math.modf(divisions / 2.0)[1] + 2 * math.modf(divisions / 2.0)[0]
        )
        is_even = 2 * math.modf((divisions + 1) / 2.0)[0]

        # fill inner points
        for k in range(0, corner_sides):
            if (k + 1) * divisions > len(outer_points) - 1:
                a = self.vertices[outer_points[0]]
            else:
                a = self.vertices[outer_points[(k + 1) * divisions]]
            if k == 0:
                b = self.vertices[outer_points[len(outer_points) - 1]]
            else:
                b = self.vertices[outer_points[k * divisions - 1]]

            if is_even == 0:  # if no even
                median = (mid[k]).lerp(
                    center, depth / float(half_start_divisions)
                )
                for i in range(0, half_divisions - 2):
                    j = half_divisions - 3 - i
                    p = median.lerp(b, 1 / half_divisions * (j + 1))
                    self.vertices.append(p)
                    inner_points.extend([len(self.vertices) - 1])

                    # new_faces[0].extend([len(self.vertices)-1])

                self.vertices.append(median)
                # new_faces[0].extend([len(self.vertices)-1])
                inner_points.extend([len(self.vertices) - 1])

                for i in range(0, half_divisions - 1):
                    p = median.lerp(a, 1 / half_divisions * (i + 1))
                    self.vertices.append(p)
                    inner_points.extend([len(self.vertices) - 1])

                    # new_faces[0].extend([len(self.vertices)-1])

            else:  # if even
                median = (mid[k]).lerp(
                    center,
                    depth * 2 * is_even / float(start_divisions + is_even),
                )
                for i in range(0, half_divisions):
                    j = half_divisions - 1 - i
                    p = median.lerp(
                        b,
                        2 / float(divisions + 1) * is_even * j
                        + 1 / float(divisions + 1) * is_even,
                    )
                    self.vertices.append(p)
                    inner_points.extend([len(self.vertices) - 1])

                    # new_faces[0].extend([len(self.vertices)-1])

                for i in range(0, half_divisions - 1):
                    p = median.lerp(
                        a,
                        2 / float(divisions + 1) * is_even * i
                        + 1 / float(divisions + 1) * is_even,
                    )
                    self.vertices.append(p)
                    inner_points.extend([len(self.vertices) - 1])

                    # new_faces[0].extend([len(self.vertices)-1])

        new_corner = []
        if is_even == 0:
            for i in range(0, corner_sides):
                we = int((i + 1) * (divisions - 1) - 1)
                new_corner.append(inner_points[we])
            new_corner = (
                new_corner[len(new_corner) - 1 :]
                + new_corner[0 : len(new_corner) - 1]
            )
        else:
            for i in range(0, corner_sides):
                we = int((i) * (divisions - 1))
                new_corner.append(inner_points[we])
        """
        print outer_points
        print inner_points
        print corner
        print new_corner
        """
        # fills sides
        k = 0
        for i in range(0, corner_sides):
            for j in range(0, divisions - 1):
                # print i*divisions+j,i*divisions+j+1,
                if is_even == 0:
                    if k - 1 >= 0:
                        new_faces.append(
                            [
                                outer_points[i * divisions + j],
                                outer_points[i * divisions + j + 1],
                                inner_points[k],
                                inner_points[k - 1],
                            ]
                        )
                    else:
                        new_faces.append(
                            [
                                outer_points[i * divisions + j],
                                outer_points[i * divisions + j + 1],
                                inner_points[k],
                                inner_points[len(inner_points) - 1],
                            ]
                        )
                else:
                    if k + 1 < len(inner_points):
                        new_faces.append(
                            [
                                outer_points[i * divisions + j],
                                outer_points[i * divisions + j + 1],
                                inner_points[k + 1],
                                inner_points[k],
                            ]
                        )
                    else:
                        new_faces.append(
                            [
                                outer_points[i * divisions + j],
                                outer_points[i * divisions + j + 1],
                                inner_points[0],
                                inner_points[k],
                            ]
                        )
                k += 1
            # fill corner faces
            if i * divisions - 1 >= 0:
                new_faces.append(
                    [
                        corner[i],
                        outer_points[i * divisions],
                        new_corner[i],
                        outer_points[i * divisions - 1],
                    ]
                )
            else:
                new_faces.append(
                    [
                        corner[i],
                        outer_points[i * divisions],
                        new_corner[i],
                        outer_points[len(outer_points) - 1],
                    ]
                )

        if divisions - 2 > 1:
            self.recursiveFillCorner(
                mid,
                new_corner,
                lists.remove_duplicates(inner_points, new_corner),
                divisions - 2,
                start_divisions,
                center,
                new_faces,
                depth + 1,
            )
        elif divisions - 2 == 1:
            self.vertices.append(center)
            mids = lists.remove_duplicates(inner_points, new_corner)
            for i in range(0, corner_sides):
                if i == corner_sides - 1:
                    new_faces.append(
                        [
                            mids[i],
                            new_corner[0],
                            mids[0],
                            len(self.vertices) - 1,
                        ]
                    )
                else:
                    new_faces.append(
                        [
                            mids[i],
                            new_corner[i + 1],
                            mids[i + 1],
                            len(self.vertices) - 1,
                        ]
                    )
        elif divisions - 2 == 0:
            new_faces.append(inner_points)

    def quadChamfer(self, sel_face):
        # ,sel_edges,width,round

        divisions = 5
        # sides = 3
        # self.faces.append([])
        # for i in range(0,sides):
        #    self.vertices.append(Point(math.sin(2*math.pi/sides*i),0,math.cos(2*math.pi/sides*i)))
        #    self.faces[0].extend([i])

        face = sel_face

        corner = self.faces[face]
        corner_sides = len(corner)

        new_faces = [[]]
        outer_points = []
        # add corner outer edges
        for i in range(0, corner_sides):
            if i == corner_sides - 1:
                v1 = self.vertices[corner[corner_sides - 1]]
                v2 = self.vertices[corner[0]]
            else:
                v1 = self.vertices[corner[i]]
                v2 = self.vertices[corner[i + 1]]
            for j in range(0, divisions):
                p = Point()
                p = v1.lerp(v2, (j + 1) / float(divisions + 1))
                self.vertices.append(p)
                outer_points.extend([len(self.vertices) - 1])

        # add corner middle vertices
        center = self.__faceCenter(face)
        mid = []
        for k in range(0, corner_sides):
            if k == corner_sides - 1:
                a = self.vertices[corner[0]]
                b = self.vertices[corner[corner_sides - 1]]
            else:
                a = self.vertices[corner[k]]
                b = self.vertices[corner[k + 1]]
            mid.append(a.lerp(b, 0.5))
        self.recursiveFillCorner(
            mid, corner, outer_points, divisions, divisions, center, new_faces
        )
        self.faces.extend(new_faces)
        self.faces.pop(face)
        print(self)

    def quadChamfer1(self, sel_edges, chamfer_size):
        edges = self.edges

        faces_involved = self.__selectConvertVF2(edges)
        vertices_involved = []
        for i in range(0, len(edges)):
            vertices_involved.append(edges[i][0])
            vertices_involved.append(edges[i][1])
        vertices_involved = list(set(vertices_involved))
        faces_terminate = self.__selectConvertVF(vertices_involved)
        faces_terminate = lists.remove_duplicates(
            faces_terminate, faces_involved
        )
        print("faces_terminate ", faces_terminate)
        print("faces_involved ", faces_involved)
        print("vertices_involved ", vertices_involved)
        chamfer_data = []

        for face in faces_involved:
            new_face = copy(self.faces[face])
            for vertex in vertices_involved:
                # print "test vertex ", vertex
                neighbors = self.findVertexNeighbor(vertex, [face])
                if len(neighbors) > 0:
                    edge_vertex = copy(neighbors)
                    neighbors = lists.remove_duplicates(
                        neighbors, vertices_involved
                    )

                    if len(neighbors) > 0:
                        # termination vertex
                        edge_vertex = lists.remove_duplicates(
                            edge_vertex, neighbors
                        )
                        neighbor = neighbors[0]
                        edge_vertex = edge_vertex[0]
                        v2 = Vector()
                        v2.fromPoints(
                            self.vertices[neighbor], self.vertices[vertex]
                        )
                        v2 = v2.normalize()
                        a = -v2.setLength(chamfer_size)
                    else:
                        # corner vertex
                        # print "edge_vertices ",edge_vertex
                        v1 = Vector()
                        v1.fromPoints(
                            self.vertices[vertex], self.vertices[edge_vertex[0]]
                        )
                        v1 = v1.normalize()

                        v2 = Vector()
                        v2.fromPoints(
                            self.vertices[edge_vertex[1]], self.vertices[vertex]
                        )
                        v2 = v2.normalize()
                        angle = v1.angle(v2)
                        a = v1 - v2
                        if angle < 0.1:
                            a = a.setLength(chamfer_size)
                        else:
                            angle_between = math.cos(angle / 2)
                            a = a.setLength(chamfer_size / angle_between)

                    self.vertices.append(self.vertices[vertex])
                    new_vertex = len(self.vertices) - 1
                    self.vertices[new_vertex].addRuler(a)
                    self.vertices[new_vertex] += self.vertices[new_vertex].ruler
                    chamfer_data.append([vertex, new_vertex])

                    repl_id = lists.find(new_face, vertex)
                    new_face[repl_id] = new_vertex

            self.faces[face] = copy(new_face)

        chamfer_data = lists.group_by_1st(chamfer_data)
        # for face in faces_involved:
        # for i in range(0,len(vertices_involved)):
        # sel = lists.find(self.faces[face],vertices_involved[])
        # print sel

        print("chamfer_data ", chamfer_data)
        print(edges)
        for chamfer_element in chamfer_data:
            if len(chamfer_element) > 3:
                self.faces.append(chamfer_element[1:])
                self.quadChamfer(len(self.faces) - 1)
            else:
                for face_t in faces_terminate:
                    repl_id = lists.find(self.faces[face_t], chamfer_element[0])

                    if repl_id != -1:
                        print(repl_id)
                        print(
                            self.faces[face_t],
                            self.faces[face_t][: repl_id - 1]
                            + chamfer_element[1:]
                            + self.faces[face_t][repl_id + 1 :],
                        )

                        self.faces[face_t] = (
                            self.faces[face_t][: repl_id - 1]
                            + chamfer_element[1:]
                            + self.faces[face_t][repl_id + 1 :]
                        )

    def insertCylinder(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        factor = kwargs.get("factor", self.selectionType)
        if selection_type != kGeotype.face:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.face
            )

        # insert rectangle, triangulate to insert not quads not implemented
        avg_normal = Vector()
        avg_center = Vector()

        for i in range(0, len(selection)):
            avg_normal = avg_normal + self.getNormal(selection[i])
            avg_center = avg_center + self.__faceCenter(selection[i])
        avg_center = avg_center / float(len(selection))
        border = self.__selectFaceBorders(selection)[0]
        corner = []
        a = Vector()
        for i in range(0, len(border)):
            if len(self.findVertexNeighbor(border[i], selection)) < 3:
                corner.append(border[i])

        # compute radius and up vector
        for i in range(len(corner)):
            if i < len(corner) - 1:
                mid = (self.vertices[corner[i]]).lerp(
                    self.vertices[corner[i + 1]], 0.5
                )
            else:
                mid = (self.vertices[corner[i]]).lerp(
                    self.vertices[corner[0]], 0.5
                )
            b = avg_center - mid
            if i == 0:
                radius = b.length()
                a = b
            else:
                radius = min(radius, b.length())
            if (a.normalize()).dot(Vector(0, 1, 0)) < (b.normalize()).dot(
                Vector(0, 1, 0)
            ):
                a = b

        t = Transform()
        t.lookAt(
            avg_center + avg_normal.normalize() * 1.2,
            avg_center + avg_normal,
            a,
        )
        interior_vertices = self.__selectFacesInterior(selection)

        new_vertices = []
        sides = len(border)
        radius = radius * factor
        even = math.modf(sides / 3.0)[0] == 0
        if even:
            t1 = Transform()
            t1.rotateZ(360 / float(sides) * 0.5)

        self.addFaces([[], []])
        # add new vertices
        cycle_rect = CycleList(lists.enumerate_list(border))
        cycle_rect.cycle(3)
        for i in range(sides):
            p = Point(
                math.sin(2 * math.pi / sides * i) * radius,
                math.cos(2 * math.pi / sides * i) * radius,
                0,
            )

            if even:
                p = t1.applyTransform(p)

            modr = math.modf(cycle_rect[i] / math.modf(sides / 4.0)[1])
            if modr[1] == 0:
                rectp = Point(-0.5 * radius, (modr[0] - 0.5) * radius, 0)
            elif modr[1] == 1:
                rectp = Point((modr[0] - 0.5) * radius, 0.5 * radius, 0)
            elif modr[1] == 2:
                rectp = Point(0.5 * radius, (0.5 - modr[0]) * radius, 0)
            elif modr[1] == 3:
                rectp = Point((0.5 - modr[0]) * radius, -0.5 * radius, 0)

            p = t.applyTransform(p)

            self.addVertex(p)

            self.faces[len(self.faces) - 2] += [len(self.vertices) - 1]

            rectp = t.applyTransform(rectp)

            self.addVertex(p)
            self.faces[len(self.faces) - 1] += [len(self.vertices) - 1]

            p = p.lerp(rectp, 1)

            # ray origin direction
            ray = Ray(p, -avg_normal.normalize())
            hitted = False
            k = 0
            while k < len(selection) and not hitted:
                j = selection[k]
                # triangulate needed
                triangle = []

                triangle.append(self.vertices[self.faces[j][0]])
                triangle.append(self.vertices[self.faces[j][2]])
                triangle.append(self.vertices[self.faces[j][1]])
                hit = ray.triangleRayHit(triangle)
                if hit != 0:
                    # print "first"
                    self.addVertex(ray.origin + ray.direction * hit[1][2])
                    new_vertices.append(len(self.vertices) - 1)
                    hitted

                triangle = []
                triangle.append(self.vertices[self.faces[j][0]])
                triangle.append(self.vertices[self.faces[j][3]])
                triangle.append(self.vertices[self.faces[j][2]])
                hit = ray.triangleRayHit(triangle)
                if hit != 0:
                    # print "second"
                    self.addVertex(ray.origin + ray.direction * hit[1][2])
                    new_vertices.append(len(self.vertices) - 1)
                    hitted
                k += 1

        new_vertices = new_vertices[::-1]

        # cycle through the lists to find nearest vertices for connection
        min_dist = 0
        min_i = 0
        min_j = 0

        for i in range(0, sides):
            for j in range(0, sides):
                new_dist = (
                    self.vertices[new_vertices[i]] - self.vertices[border[j]]
                ).length()
                if i == 0 and j == 0:
                    min_dist = new_dist
                if min_dist > new_dist:
                    min_dist = new_dist
                    min_i = i
                    min_j = j
        border = lists.cycle(border, min_j)
        new_vertices = lists.cycle(new_vertices, min_i)

        # add new faces
        new_faces = []
        for i in range(0, sides):
            if i < sides - 1:
                new_faces.append(
                    [
                        border[i],
                        border[i + 1],
                        new_vertices[i + 1],
                        new_vertices[i],
                    ]
                )
            else:
                new_faces.append(
                    [border[i], border[0], new_vertices[0], new_vertices[i]]
                )

        self.addFaces(new_faces)

        # delete unused vertices and faces
        self.__deleteVertices(interior_vertices)
        self.__deleteFaces(selection)
        return [kResult.updateMesh]

    def capParallel(self, selection, **kwargs):
        selection_type = kwargs.get("selection_type", self.selectionType)
        if selection_type != kGeotype.face:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.face
            )

        for face_id in selection:
            face = self.faces[face_id]
            max_id = 0
            len_max = 0
            for i in range(0, len(face) - 1):
                v1 = Vector()
                v1.fromPoints(
                    self.vertices[face[i]], self.vertices[face[i + 1]]
                )
                length = v1.length()
                if len_max < length:
                    len_max = length
                    max_id = i

            self.updateFace(
                face_id, lists.cycle(self.faces[face_id], max_id + 2)
            )
            for i in range(0, math.modf(len(face) / 2.0)[1] - 1):
                # print "connect pairs"

                if i == 0:
                    self.addFace(
                        [
                            face[i],
                            face[len(face) - 3 - i],
                            face[len(face) - 3 - i + 1],
                            face[len(face) - 1],
                        ]
                    )
                    # print (face[i],face[len(face)-3-i],face[len(face)-3-i+1],face[len(face)-1])
                    # print i,len(face)-3-i,len(face)-3-i+1,len(face)-1
                else:
                    self.addFace(
                        [
                            face[i],
                            face[len(face) - 3 - i],
                            face[len(face) - 3 - i + 1],
                            face[i - 1],
                        ]
                    )
                    # print (face[i],face[len(face)-3-i],face[len(face)-3-i+1],face[i-1])

            if math.modf(len(face) / 2.0)[0] == 0.5:
                i = int(math.modf(len(face) / 2.0)[1] - 2)
                self.addFace([face[i], face[i + 1], face[len(face) - 3 - i]])
                # print (face[i],face[i+1],face[len(face)-3-i])
        self.__deleteFaces(selection)
        return [kResult.updateMesh]

    def extrude(self, selection, **kwargs):
        # TODO Coplanar edges in a row not implemented
        # TODO implement faces interior extrude
        selection_type = kwargs.get("selection_type", self.selectionType)
        height = kwargs.get("height", 0)
        inset = kwargs.get("inset", 0)

        if selection_type != kGeotype.face:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.face
            )

        borders = self.__selectFaceBordersEx(selection)

        borders.append([])
        # borders[0] - vertex border | borders[1] - faces border | borders[2] - rejected pairs | borders[3] - new vertices
        for f in range(0, len(borders[0])):
            borders[3].append([])
            # add vertices
            for k in borders[0][f]:
                self.addVertex(self.vertices[k])
                # self.vertices.append(self.vertices[k])
                borders[3][len(borders[3]) - 1].extend([len(self.vertices) - 1])
            # print borders

            # update cap faces
            for j in borders[1][f]:
                # print self.faces[j]
                for k in range(0, len(self.faces[j])):
                    dup = lists.duplicates_of(borders[0][f], self.faces[j][k])
                    if len(dup) >= 1:
                        self.__updateFaceVert(j, k, borders[3][f][dup[0]])
                        # self.faces[j][k] = borders[3][f][dup[0]]
                # print self.faces[j]

            # add side faces
            borders[0][f].append(borders[0][f][0])
            borders[3][f].append(borders[3][f][0])
            for i in range(1, len(borders[0][f])):
                self.addFace(
                    [
                        borders[0][f][i - 1],
                        borders[0][f][i],
                        borders[3][f][i],
                        borders[3][f][i - 1],
                    ]
                )

            # update vertex rulers

            borders_rejected = []
            for i in range(0, len(borders[2])):
                borders_rejected.append(borders[2][i][0])

            for i in range(1, len(borders[0][f])):
                v1 = Vector()
                v2 = Vector()
                if i < len(borders[0][f]) - 1:
                    v1.fromPoints(
                        self.vertices[borders[3][f][i]],
                        self.vertices[borders[3][f][i - 1]],
                    )
                    v2.fromPoints(
                        self.vertices[borders[3][f][i + 1]],
                        self.vertices[borders[3][f][i]],
                    )
                else:
                    v1.fromPoints(
                        self.vertices[borders[3][f][i]],
                        self.vertices[borders[3][f][i - 1]],
                    )
                    v2.fromPoints(
                        self.vertices[borders[3][f][1]],
                        self.vertices[borders[3][f][i]],
                    )
                v1 = v1.normalize()
                v2 = v2.normalize()
                dup = lists.duplicates_of(borders_rejected, borders[0][f][i])
                if len(dup) >= 1:
                    c = []
                    for j in dup:
                        c.append(
                            (
                                self.vertices[borders[2][j][1]]
                                - self.vertices[borders[2][j][0]]
                            ).normalize()
                        )
                    b = Vector()
                    angleb = 0
                    for j in range(0, len(c)):
                        angleb = max(c[0].angle(c[j]), angleb)
                        b = b + c[j]
                    b.normalize()
                    a = b.cross(v1) + b.cross(v2)
                    anglea = a.angle(v1) - math.pi / 2.0
                    # print(math.degrees(anglea))
                    if angleb < 0.1:
                        b = b.setLength(inset)
                    else:
                        angle_between = math.cos(angleb / 2)
                        b = b.setLength(inset / angle_between)
                    if anglea < 0.05 and anglea > -0.05:
                        a = a.setLength(height)
                    else:
                        angle_between = math.cos(anglea)
                        a = a.setLength(height / angle_between)
                    self.vertices[borders[3][f][i]].addRuler(b + a)
                    continue

                anglea = v1.angle(v2)
                # print angle_between
                print(anglea)
                a = v1.cross(v2)
                a = a.setLength(height)
                if anglea < 0.1:
                    b = (v1 - v2).setLength(inset)
                # elif angle_between==1:
                #    b = Vector()
                else:
                    angle_between = math.cos(anglea / 2)
                    b = (v1 - v2).setLength(inset / angle_between)
                self.vertices[borders[3][f][i]].addRuler(b + a)

            # update vertex positions
            for i in range(1, len(borders[3][f])):
                self.updateVertex(
                    borders[3][f][i],
                    self.vertices[borders[3][f][i]]
                    + self.vertices[borders[3][f][i]].ruler,
                )
                # self.vertices[borders[3][f][i]] += self.vertices[borders[3][f][i]].ruler
        return [kResult.updateMesh]

    def capCylinder(self, faces):
        # automatic orientation not implemented

        for face in faces:
            sides = len(self.faces[face])
            verts_count_old = len(self.vertices)
            print("sides")
            print(sides)
            modulo = math.modf(((sides - 4) / 4.0) / 1)
            less_sides = int(modulo[1])
            more_sides = less_sides + 1
            if modulo[0] == 0.0 or modulo[0] == 0.25:
                more_sides = less_sides
            less_sides - 2
            print("divisions")
            print(more_sides, less_sides)
            more_connections = []
            print("connections " + str(more_sides))
            for i in range(0, more_sides):
                c = more_sides * 2 - i + 1 + less_sides
                print(self.faces[face][i], self.faces[face][c])
                more_connections.append(
                    [self.faces[face][i], self.faces[face][c]]
                )
            # add points
            for i in more_connections:
                for j in range(1, less_sides + 1):
                    a = self.vertices[i[0]].lerp(
                        self.vertices[i[1]], j / float(less_sides + 1)
                    )
                    self.addVertex(Point(a.x, a.y, a.z))

            # connect faces
            print("left")
            for i in range(1, more_sides):
                w = [
                    self.faces[face][i],
                    less_sides * i + verts_count_old,
                    less_sides * (i - 1) + verts_count_old,
                    self.faces[face][i - 1],
                ]
                print(w)
                self.addFace(w)
            print("top")
            for i in range(more_sides + 2, more_sides + 1 + less_sides):
                w = [
                    self.faces[face][i],
                    more_sides * less_sides
                    - less_sides
                    - more_sides
                    - 1
                    + i
                    + verts_count_old,
                    more_sides * less_sides
                    - less_sides
                    - more_sides
                    - 2
                    + i
                    + verts_count_old,
                    self.faces[face][i - 1],
                ]
                print(w)
                self.addFace(w)
            print("right")
            for i in range(
                more_sides + less_sides + 3,
                more_sides + more_sides + less_sides + 2,
            ):
                w = [
                    self.faces[face][i],
                    2 * less_sides * more_sides
                    - (i - less_sides - 2) * less_sides
                    - 1
                    + verts_count_old,
                    less_sides * (2 * more_sides - i + less_sides + 3)
                    - 1
                    + verts_count_old,
                    self.faces[face][i - 1],
                ]
                print(w)
                self.addFace(w)
            print("bottom")
            for i in range(
                more_sides * 2 + less_sides + 4,
                more_sides * 2 + less_sides + 3 + less_sides,
            ):
                w = [
                    self.faces[face][i],
                    less_sides * 2 + more_sides * 2 + 2 - i + verts_count_old,
                    less_sides * 2 + more_sides * 2 + 3 - i + verts_count_old,
                    self.faces[face][i - 1],
                ]
                print(w)
                self.addFace(w)
            print("grid")
            for i in range(1, more_sides):
                for j in range(1, less_sides):
                    w = [
                        j + (i - 1) * less_sides - 1 + verts_count_old,
                        less_sides * i + j - 1 + verts_count_old,
                        less_sides * i + j + verts_count_old,
                        j + (i - 1) * less_sides + verts_count_old,
                    ]
                    print(w)
                    self.addFace(w)
            print("corners")
            w = [
                self.faces[face][more_sides - 1],
                self.faces[face][more_sides],
                self.faces[face][more_sides + 1],
                more_sides * less_sides
                - more_sides
                + (more_sides + 1) % (less_sides + 1)
                + verts_count_old,
            ]
            print(w)
            self.addFace(w)
            w = [
                self.faces[face][more_sides + less_sides],
                self.faces[face][more_sides + less_sides + 1],
                self.faces[face][more_sides + less_sides + 2],
                more_sides * less_sides - 1 + verts_count_old,
            ]
            print(w)
            self.addFace(w)
            w = [
                self.faces[face][2 * more_sides + less_sides + 1],
                self.faces[face][2 * more_sides + less_sides + 2],
                self.faces[face][2 * more_sides + less_sides + 3],
                less_sides - 1 + verts_count_old,
            ]
            print(w)
            self.addFace(w)
            if math.modf(sides / 2.0)[0] != 0:
                w = [
                    self.faces[face][2 * more_sides + 2 * less_sides + 2],
                    self.faces[face][2 * more_sides + 2 * less_sides + 3],
                    verts_count_old,
                ]
                print(w)
                self.addFace(w)
                print("not even")
                w = [
                    self.faces[face][2 * more_sides + 2 * less_sides + 3],
                    self.faces[face][2 * more_sides + 2 * less_sides + 4],
                    self.faces[face][0],
                    verts_count_old,
                ]
                print(w)
                self.addFace(w)
            else:
                w = [
                    self.faces[face][2 * more_sides + 2 * less_sides + 2],
                    self.faces[face][2 * more_sides + 2 * less_sides + 3],
                    self.faces[face][0],
                    verts_count_old,
                ]
                print(w)
                self.addFace(w)

            self.__deleteFaces([face])
            grid_vertices = []
            for i in range(
                len(self.vertices) - less_sides * more_sides, len(self.vertices)
            ):
                grid_vertices.append(i)
            # self.relax(grid_vertices,1,10)
        return [kResult.updateMesh]

    def straightLoop(self, sel_edges):
        borders = self.__selectEdgesGroups(sel_edges)
        t1 = Transform()
        t2 = Transform()
        for border in borders:
            v = Vector()

            for i in range(len(border) - 1):
                v += self.vertices[border[i]] - self.vertices[border[i + 1]]
            center = self.vertices[border[0]].lerp(
                self.vertices[border[-1]], 0.5
            )
            v = v.normalize()
            axis = Vector(0, 1, 0)
            vcross = v.cross(axis).normalize()
            if vcross.length() == 0:
                axis = Vector(1, 0, 0)
                vcross = v.cross(axis).normalize()
            # self.addVertex(center)
            # self.addVertex(center+vcross)
            # self.addVertex(center+v.cross(vcross))
            t1.scaleLocal(0, center, vcross)
            t2.scaleLocal(0, center, v.cross(vcross).normalize())
            t1 = t1 * t2
            for i in range(len(border)):
                self.updateVertex(
                    border[i], t1.applyTransform(self.vertices[border[i]])
                )
        return [kResult.updateVertex]

    def scaleGroups(self, selection, scale, **kwargs):
        # TODO group for faces and edges
        selection_type = kwargs.get("selection_type", self.selectionType)
        if selection_type != kGeotype.vertex:
            selection = self.selectConvert(
                selection, selection_type, kGeotype.vertex
            )
        borders = self.__selectVertexGroups(selection)
        for border in borders:
            mid = Point()
            for vert in border:
                mid += self.vertices[vert]
            mid = mid / len(border)
            self.addVertex(mid)
            t = Transform()
            t.translate(-mid)
            ts = Transform()
            ts.scale(Vector(scale, scale, scale))
            for vert in border:
                p = ts.applyTransform(t.applyTransform(self.vertices[vert]))
                t.invert()
                p = t.applyTransform(p)
                self.updateVertex(vert, p)
                t.invert()
        return [kResult.updateVertex]

    def flowLoop(self, sel_edges, factor=1):
        def list_1dimension(lst):
            n = []
            for i in range(len(lst)):
                n += lst[i]
            return n

        borders = self.__selectEdgesGroups(sel_edges)
        for border in borders:
            anchors = self.__selectLoopGroupAnchors(border)
            border1 = lists.get_row(anchors, 0)
            border2 = lists.get_row(anchors, 1)
            anchors1 = self.__selectLoopGroupAnchors(border1)
            anchors2 = self.__selectLoopGroupAnchors(border2)
            anchors1 = lists.remove_duplicates(
                list_1dimension(anchors1), border
            )
            anchors2 = lists.remove_duplicates(
                list_1dimension(anchors2), border
            )

            for i in range(len(border)):
                # print anchors1[i],anchors[i][0],anchors[i][1],anchors2[i]
                v1 = self.vertices[anchors1[i]]
                v2 = self.vertices[anchors[i][0]]
                self.vertices[border[i]]
                v4 = self.vertices[anchors[i][1]]
                v5 = self.vertices[anchors2[i]]
                p0 = v1.lerp(v2, 0.5)
                p1 = v2.lerp(v1, -0.5)
                p2 = v4.lerp(v5, -0.5)
                p3 = v4.lerp(v5, 0.5)
                # self.addVertex(p0)
                # self.addVertex(p1)
                # self.addVertex(p2)
                # self.addVertex(p3)
                p = interpolateBezier(0.5, p0, p1, p2, p3)
                self.updateVertex(
                    border[i], self.vertices[border[i]].lerp(p, factor)
                )
                # for j in range(11):
                #    pi = interpolateBezier(j/10.2,p0,p1,p2,p3)
                #    self.addVertex(pi)
        return [kResult.updateVertex]

    def slideLoop(self, sel_edges, percent=0.5):
        borders = self.__selectEdgesGroups(sel_edges)
        for border in borders:
            anchors = self.__selectLoopGroupAnchors(border)
            for i in range(len(border)):
                if percent > 0:
                    self.updateVertex(
                        border[i],
                        self.vertices[border[i]].lerp(
                            self.vertices[anchors[i][0]], percent
                        ),
                    )
                else:
                    self.updateVertex(
                        border[i],
                        self.vertices[border[i]].lerp(
                            self.vertices[anchors[i][1]], -percent
                        ),
                    )
        return [kResult.updateVertex]

    def spaceLoops(self, sel_edges):
        borders = self.__selectEdgesGroups(sel_edges)
        for border in borders:
            avg_len = 0
            for i in range(1, len(border)):
                avg_len += (
                    self.vertices[border[i - 1]] - self.vertices[border[i]]
                ).length()
            avg_len = avg_len / (len(border) - 1)
            for i in range(1, len(border) - 1):
                edge_v = (
                    self.vertices[border[i]] - self.vertices[border[i - 1]]
                ).setLength(avg_len / 2.0)
                edge_center = self.vertices[border[i]].lerp(
                    self.vertices[border[i - 1]], 0.5
                )
                self.updateVertex(border[i], edge_center + edge_v)
                self.updateVertex(border[i - 1], edge_center - edge_v)
        return [kResult.updateVertex]

    def centerLoops(self, sel_edges, ellipse_interpolation=False):
        borders = self.__selectEdgesGroups(sel_edges)
        for border in borders:
            anchors = self.__selectLoopGroupAnchors(border)
            for i in range(len(border)):
                # determine ellipse b coefficient
                c = self.vertices[border[i]]
                a = self.vertices[anchors[i][0]]
                b = self.vertices[anchors[i][1]]
                alpha = (a - c).angle((a - b))
                if alpha > EPSILON or alpha < -EPSILON:
                    x = (a - c).length() * math.cos(alpha)
                    y = (a - c).length() * math.sin(alpha)
                    if ellipse_interpolation:
                        height = (
                            y
                            * y
                            / (1 - x * x / (a - b).length() / (a - b).length())
                        ) ** 0.5
                    else:
                        height = y / 2
                else:
                    x = (a - c).length() / (a - b).length()
                    y = 0
                    height = 0
                self.updateVertex(
                    border[i],
                    a.lerp(b, 0.5)
                    - ((a - c) - (a - b).setLength(x)).setLength(height),
                )
        return [kResult.updateVertex]

    def collapseEdges(self, sel_edges):
        delete_faces = []
        delete_verts = []
        borders = self.__selectEdgesGroups(sel_edges)
        for border in borders:
            delete_verts += border
            center = Point()
            for vert in border:
                center += self.vertices[vert]
            center /= len(border)
            self.addVertex(center)
            new_id = len(self.vertices) - 1
            faces = self.__selectConvertVF(border)
            for face in faces:
                for vert in border:
                    find = lists.find(self.faces[face], vert)
                    if find > -1:
                        self.__updateFaceVert(face, find, new_id)
                self.updateFace(face, lists.group_duplicates(self.faces[face]))
                if len(self.faces[face]) < 3:
                    delete_faces += [face]
        delete_verts = lists.group_duplicates(delete_verts)
        self.__deleteVertices(delete_verts)
        if len(delete_faces) > 0:
            delete_faces = lists.group_duplicates(delete_faces)
            self.__deleteFaces(delete_faces)
        return [kResult.updateMesh]

    def splitEdges(self, sel_edges):
        # TODO split faces
        borders = self.__selectEdgesGroups(sel_edges)
        for border in borders:
            # print border
            faces = self.__selectConvertVF(border)
            face_left = copy(self.faces[faces[0]])
            face_left_ids = [faces[0]]
            face_right = []
            face_right_ids = []
            for i in range(1, len(faces)):
                for vert in self.faces[faces[i]]:
                    if vert not in border:
                        find = lists.find(face_left, vert)
                        if find != -1:
                            if faces[i] not in face_left_ids:
                                face_left.extend(self.faces[faces[i]])
                                face_left_ids.append(faces[i])
                        else:
                            if faces[i] not in face_right_ids:
                                face_right.extend(self.faces[faces[i]])
                                face_right_ids.append(faces[i])
            # print face_left_ids,face_right_ids
            new_border = lists.enumerate_list(border, len(self.vertices))
            for i in range(len(border)):
                self.addVertex(self.vertices[border[i]])
            for i in face_right_ids:
                upd_face = copy(self.faces[i])
                for j in range(len(upd_face)):
                    find = lists.find(border, upd_face[j])
                    if find != -1:
                        upd_face[j] = new_border[find]
                self.updateFace(i, upd_face)
        return [kResult.updateMesh]

    def connectEdges(self, sel_edges, connections=1):
        # TODO sometimes wrong connections
        new_edges = []

        for i in range(len(sel_edges)):
            new_edges.append([])
            for j in range(0, connections):
                v1 = self.edges[sel_edges[i]][0]
                v2 = self.edges[sel_edges[i]][1]
                center = self.vertices[v1].lerp(
                    self.vertices[v2], 1 / float(connections + 1) * (j + 1)
                )
                self.addVertex(center)
                new_edges[i].extend([len(self.vertices) - 1])
        new_faces = []
        passed_faces = []
        delete_faces = []
        for i in range(len(sel_edges)):
            faces = self.__selectConvertEF([sel_edges[i]])
            for face in faces:
                if face not in passed_faces:
                    edges = self.__selectConvertFE([face])
                    for edge in edges:
                        self.updateFace(
                            face, self.faces[face] + new_edges[edge]
                        )
                    self.updateFace(
                        face, self.__sortVerticesCCW(self.faces[face])
                    )
                    passed_faces += [face]
                    # edge crosses not implemented
                    if len(edges) == 2:
                        face_cycle = CycleList(self.faces[face])
                        first = face_cycle.find(new_edges[edges[0]][0])
                        face_cycle.cycle(first)
                        first_last = face_cycle.find(
                            new_edges[edges[0]][connections - 1]
                        )
                        if first_last > connections + 1:
                            first = first_last
                            face_cycle.cycle(first)
                        self.updateFace(face, face_cycle.list)
                        first = 0
                        second = max(
                            face_cycle.find(new_edges[edges[1]][0]),
                            face_cycle.find(
                                new_edges[edges[1]][connections - 1]
                            ),
                        )
                        new_faces.extend(
                            self.__connectFace(face, first, second, connections)
                        )
                        delete_faces += [face]

        self.addFaces(new_faces)
        self.__deleteFaces(delete_faces)
        return [kResult.updateMesh]


if __name__ == "__main__":
    we = OBBox()
    p = [
        Vector(0, 1, 0),
        Vector(0, 1, 1),
        Vector(0.5, 1, 1),
        Vector(0.5, 1, 0),
        Vector(0, 0, 0),
        Vector(0, 0, 1),
        Vector(0.5, 0, 1),
        Vector(0.5, 0, 0),
    ]
    we.fromPointSet(p)
    print(we.vectors)
    we = BBox()
    we.obbFromPointSet(p)
    print(we.axis)
