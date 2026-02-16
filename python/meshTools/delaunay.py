from geometry import *
from random import random


class Tetra(object):
    def __init__(self, v0, v1, v2, v3):  #
        self.vertices = [v0, v1, v2, v3]
        self.child = []
        self.parent = []
        self.circumcenter = Point()
        self.circumradius = 0
        self.center = (v0 + v1 + v2 + v3) / 4

        self.num = 0
        t = Transform()
        t.m = [
            v0.toList() + [1],
            v1.toList() + [1],
            v2.toList() + [1],
            v3.toList() + [1],
        ]
        self.determinant = t.determinant()
        self.calculateCircumsphere()

    def calculateCircumsphere(self):
        v0, v1 = self.vertices[0], self.vertices[1]
        v2, v3 = self.vertices[2], self.vertices[3]
        v0_len = v0.lengthSquared()
        v1_len = v1.lengthSquared()
        v2_len = v2.lengthSquared()
        v3_len = v3.lengthSquared()
        t = Transform()
        a = 2 * self.determinant
        t.m = [
            [v0_len, v0.y, v0.z, 1],
            [v1_len, v1.y, v1.z, 1],
            [v2_len, v2.y, v2.z, 1],
            [v3_len, v3.y, v3.z, 1],
        ]
        d0 = t.determinant()
        t.m = [
            [v0_len, v0.x, v0.z, 1],
            [v1_len, v1.x, v1.z, 1],
            [v2_len, v2.x, v2.z, 1],
            [v3_len, v3.x, v3.z, 1],
        ]
        d1 = -t.determinant()
        t.m = [
            [v0_len, v0.x, v0.y, 1],
            [v1_len, v1.x, v1.y, 1],
            [v2_len, v2.x, v2.y, 1],
            [v3_len, v3.x, v3.y, 1],
        ]
        d2 = t.determinant()
        self.circumcenter = Point(d0 / a, d1 / a, d2 / a)
        self.circumradius = (self.circumcenter - v0).length()
        # print self.circumcenter,self.circumradius

    def __getitem__(self, key):
        return self.vertices[key]

    def __setitem__(self, key, value):
        self.vertices[key] = value

    def __str__(self):
        s = ""
        for vert in self.vertices:
            s = s + " " + str(vert.num)
        return "[" + s + "]"


class Delaunay(object):
    def addTetrahedra(self, v, tetra, case):
        t = tetra
        if case == 0:
            self.vertices += [v]
            v.num = len(self.vertices) - 1
            nt0 = Tetra(t[0], t[1], t[2], v)

            nt1 = Tetra(t[0], t[1], v, t[3])
            nt2 = Tetra(t[0], v, t[2], t[3])
            nt3 = Tetra(v, t[1], t[2], t[3])
            nt0.parent, nt1.parent, nt2.parent, nt3.parent = (
                tetra,
                tetra,
                tetra,
                tetra,
            )
            tetra.child += [nt0, nt1, nt2, nt3]

            self.tetras += [nt0, nt1, nt2, nt3]

    def pointInTetrahedra(self, v, tetra):
        t = Transform()
        v0 = tetra[0]
        v1 = tetra[1]
        v2 = tetra[2]
        v3 = tetra[3]
        d = tetra.determinant
        t.m = [
            v.toList() + [1],
            v1.toList() + [1],
            v2.toList() + [1],
            v3.toList() + [1],
        ]
        d0 = t.determinant()
        t.m = [
            v0.toList() + [1],
            v.toList() + [1],
            v2.toList() + [1],
            v3.toList() + [1],
        ]
        d1 = t.determinant()
        t.m = [
            v0.toList() + [1],
            v1.toList() + [1],
            v.toList() + [1],
            v3.toList() + [1],
        ]
        d2 = t.determinant()
        t.m = [
            v0.toList() + [1],
            v1.toList() + [1],
            v2.toList() + [1],
            v.toList() + [1],
        ]
        d3 = t.determinant()
        # print(d,d1,d2,d3,d4)
        if d == 0:
            print("degenerate tetrahedra")
        elif (d > 0 and d0 > 0 and d1 > 0 and d2 > 0 and d3 > 0) or (
            d < 0 and d0 < 0 and d1 < 0 and d2 < 0 and d3 < 0
        ):
            print(len(self.vertices), "point in tetrahedra")
            self.addTetrahedra(v, tetra, 0)
        else:
            if d0 == 0:
                print("point lies on boundary v1,v2,v3")
            if d1 == 0:
                print("point lies on boundary v0,v2,v3")
            if d2 == 0:
                print("point lies on boundary v0,v1,v3")
            if d3 == 0:
                print("point lies on boundary v0,v1,v2")
        # else: print("point outside")

        # If by chance the D0=0, then your tetrahedr is degenerate (the points are coplanar).
        # If any other Di=0, then P lies on boundary i (boundary i being that boundary formed by the three points other than Vi).
        # If the sign of any Di differs from that of D0 then P is outside boundary i.
        # If the sign of any Di equals that of D0 then P is inside boundary i.
        # If P is inside all 4 boundaries, then it is inside the tetrahedr.
        # As a check, it must be that D0 = D1+D2+D3+D4.
        # The pattern here should be clear; the computations can be extended to simplicies of any dimension. (The 2D and 3D case are the triangle and the tetrahedron).
        # If it is meaningful to you, the quantities bi = Di/D0 are the usual barycentric coordinates.
        # Comparing signs of Di and D0 is only a check that P and Vi are on the same side of boundary i.

    def __init__(self, vertices, max):
        self.orig_vertices = vertices
        k = 3 * max
        v0, v1, v2, v3 = (
            Point(k, 0, 0),
            Point(-k, k, 0),
            Point(0, 0, k),
            Point(0, -2 * k, 0),
        )
        v0.num, v1.num, v2.num, v3.num = 0, 1, 2, 3
        self.vertices = [v0, v1, v2, v3]
        self.tetras = [Tetra(v0, v1, v2, v3)]

        for vert in self.orig_vertices:
            self.pointInTetrahedra(vert, self.tetras[0])

    def __str__(self):
        s = ""
        for i in self.vertices:
            s = s + " " + str(i)
        t = ""
        for i in self.tetras:
            t = t + " " + str(i)

        # for i in self.tetra_child:
        #    tc = tc+" "+str(i)

        # for i in self.tetra_parent:
        #    tp = tp+" "+str(i)
        return (
            "vertex count: "
            + str(len(self.vertices))
            + "\nvertices: "
            + s
            + "\ntetrahedrons count: "
            + str(len(self.tetras))
            + "\ntetrahedrons: "
            + t
        )  # \
        # +"\ntetra_childs: "+str(len(self.tetra_child))+"\ntetra_childs: "+tc\
        # +"\ntetra_parent: "+str(len(self.tetra_parent))+"\ntetra_parent: "+tp\


if __name__ == "__main__":
    verts = []
    min, max = -10, 10
    for i in range(20):
        r = random()
        verts += [
            Point(
                fit(random(), 0, 1, min, max),
                fit(random(), 0, 1, min, max),
                fit(random(), 0, 1, min, max),
            )
        ]
    d = Delaunay(verts, max)

    print(d)
    # w = d.computeCircumsphere(1)
    # print(w[0],w[1])
