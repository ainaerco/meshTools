"""Ear-cutting polygon triangulation.

Triangulates planar polygons by repeatedly clipping convex ears until
only a triangle remains. Handles both convex and concave polygons.
"""

from __future__ import annotations

from copy import copy

from .geometry import EPSILON


class Polygon:
    """Planar polygon with ear-cutting triangulation support."""

    def __init__(
        self,
        vertices: list,
        polygon: list[int],
        normal,
    ) -> None:
        """Build polygon from vertices list, polygon indices, and face normal.

        Args:
            vertices: List of vertex positions (Vector-like).
            polygon: Indices into vertices for polygon boundary.
            normal: Face normal vector.
        """
        self.vertex = vertices
        self.indices = []
        self.vertex_count = len(polygon)
        for i in range(self.vertex_count):
            self.indices.append(i)
        self.normal = normal
        self.orig_polygon = copy(polygon)
        self.orig_vertex_count = int(self.vertex_count)

    def triangulateIndices(self) -> list[list[int]]:
        """Triangulate the polygon using ear-cutting.

        Returns:
            List of triangles, each [v0, v1, v2] as orig_polygon indices.
        """
        triangles = []
        old_count = self.orig_vertex_count - 2
        while self.vertex_count > 3 and old_count > 0:
            old_count -= 1
            i = 1
            while i < self.vertex_count - 1:
                test = self.convexTest(i)
                # convex
                if test == 1:
                    if not self.isAnyPointInside(i):
                        triangles.append(
                            [
                                self.indices[i - 1],
                                self.indices[i],
                                self.indices[i + 1],
                            ]
                        )
                        self.removeVertex(i)
                # concave
                # elif test==0:pass
                # degenerate
                # elif test==-1:pass
                i += 1

        # self.orig_edges=[]
        # self.interior_edges=[]
        # for i in range(0,self.orig_vertex_count-1):
        #     self.orig_edges.append([self.orig_polygon[i],self.orig_polygon[i+1]])

        triangles.append(self.indices)
        for i in range(len(triangles)):
            triangles[i][0] = self.orig_polygon[triangles[i][0]]
            triangles[i][1] = self.orig_polygon[triangles[i][1]]
            triangles[i][2] = self.orig_polygon[triangles[i][2]]
        # print self.indices
        # print self.triangles
        # for i in range(0,len(self.triangles)):
        #    for j in range(2):
        #        if not [self.triangles[i][j],self.triangles[i][j+1]] in self.orig_edges:
        #            self.interior_edges.append([self.triangles[i][j],self.triangles[i][j+1]])

        # print self.orig_edges
        # print self.interior_edges
        return triangles

    def removeVertex(self, i: int) -> None:
        """Remove vertex at index i from the working vertex list.

        Args:
            i: Vertex index to remove.
        """
        for j in range(i + 1, self.vertex_count):
            self.indices[j - 1] = self.indices[j]
        self.indices.pop(self.vertex_count - 1)
        self.vertex_count -= 1

    def isAnyPointInside(self, i: int) -> bool:
        """Check if any other vertex lies inside the ear triangle at index i.

        Args:
            i: Vertex index (potential ear tip).

        Returns:
            True if any vertex is inside the ear triangle.
        """
        for j in range(self.vertex_count):
            if i != j and self.isPointInside(
                self.vertex[self.indices[j]], self.vertex[self.indices[i + 1]]
            ):
                return True
        return False

    def isPointInside(self, point, q) -> bool:
        """Barycentric test: is point inside triangle (e0, e1, q)?

        Args:
            point: Point to test.
            q: Third triangle vertex (e0, e1 from convexTest).

        Returns:
            True if point is inside.
        """
        pmq = point - q
        ntmp = pmq.cross(self.e1)

        b0 = self.mn.dot(ntmp)
        if b0 <= 0:
            return False

        ntmp = self.e0.cross(pmq)

        b1 = self.mn.dot(ntmp)
        if b1 <= 0:
            return False
        if self.ma - b0 - b1 > 0:
            return True
        else:
            return False

    def convexTest(self, i: int) -> int:
        """Classify vertex at index i as convex, concave, or degenerate.

        Args:
            i: Vertex index to test.

        Returns:
            1 (convex), 0 (concave), or -1 (degenerate).
        """
        self.e0 = (
            self.vertex[self.indices[i - 1]] - self.vertex[self.indices[i + 1]]
        )
        self.e1 = (
            self.vertex[self.indices[i]] - self.vertex[self.indices[i + 1]]
        )
        self.mn = self.e0.cross(self.e1)
        self.ma = self.mn.lengthSquared()
        # degenerate
        if -EPSILON < self.ma and self.ma < EPSILON:
            return -1
        # concave
        if self.mn.dot(self.normal) < 0:
            return 0
        # convex
        else:
            return 1
