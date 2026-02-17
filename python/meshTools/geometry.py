# Prefer package-internal extension (pip install); fall back to top-level (dev with build on path)
try:
    from ._geometry import (
        BBox,
        Transform,
        Vector,
        Ray,
        Polygon,
        epsilonTest,
        pointInPoly,
        interpolateBezier,
        interpolateCatmullRom,
        lerp,
        solveCubic,
        fit,
        min,
        max,
        getBarycentric,
        sortedVectorArray,
    )
except ImportError:
    from _geometry import (
        BBox,
        Transform,
        Vector,
        Ray,
        Polygon,
        epsilonTest,
        pointInPoly,
        interpolateBezier,
        interpolateCatmullRom,
        lerp,
        solveCubic,
        fit,
        min,
        max,
        getBarycentric,
        sortedVectorArray,
    )

# Backward compatibility: OBBox was used in mesh.py for oriented bbox
OBBox = BBox

__all__ = [
    "BBox",
    "OBBox",
    "EPSILON",
    "Point",
    "Polygon",
    "Ray",
    "Transform",
    "Vector",
    "epsilonTest",
    "fit",
    "getBarycentric",
    "interpolateBezier",
    "interpolateCatmullRom",
    "lerp",
    "max",
    "min",
    "pointInPoly",
    "solveCubic",
    "sortedVectorArray",
]

EPSILON = 0.000001


class Point(Vector):
    def __init__(self, *args):
        if len(args) == 0:
            xx, yy, zz = 0, 0, 0
        elif len(args) == 1:
            xx = args[0][0]
            yy = args[0][1]
            zz = args[0][2]
        elif len(args) == 3:
            xx = args[0]
            yy = args[1]
            zz = args[2]
        else:
            raise ValueError("Point expects 0, 1, or 3 arguments")
        Vector.__init__(self, float(xx), float(yy), float(zz))
        self.parent_faces = []

    def addRuler(self, other):
        self.ruler = other


if __name__ == "__main__":
    t = Transform()
    # t = t.lookAt(Vector(1,0,0),Vector(0,0,1),Vector(0,1,0))
    # t = t.scaleLocal(0.5,Vector(1,0,0),Vector(1,0,1).normalize())
    # t = t.rotateAxis(1.4,Vector(0,1,0))
    # t = t.invert()
    # print t
    # print 'euler',t.getEuler()

    # v1 = Vector(1,0,0)
    # t.lookAt(Vector(0,0,0),Vector(1,0,0.5),Vector(0,1,0))
    # print t
    # v1.applyTransform(t)
    # print 'v1',v1

    # #we = OBBox()
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
    # #we.fromPointSet(p)
    # #print we.vectors
    we = BBox()
    we.obbFromPointSet(p)

    # print we.axis
    t = Transform(we.axis[0], we.axis[1], we.axis[2])
    z = Transform()
    z = z * t
    z = Transform()
    z = t
    # z = t.getEuler()
    v1 = Vector(0, 0, 1)
    v2 = Vector(0, 1, 0)
    v3 = Vector(1, 0, 0)
    v1 += v2
    v1 -= v2
    # print degrees(z[0]),degrees(z[1]),degrees(z[2])

    # print we.max[0]-we.min[0]
    # print we.max[1]-we.min[1]
    # print we.max[2]-we.min[2]
    # print "center",we.center

    # v = Vector(0,0,0)
    # p = [Vector(1,0,0),Vector(-1,-0.001,0),Vector(0,1,0)]

    # print pointInPoly(v,p)
