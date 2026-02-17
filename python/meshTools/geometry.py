"""Geometry module: vectors, transforms, bounding boxes, rays, polygons.

Exposes C extension primitives when available (_geometry), otherwise imports
from the top-level build. Provides Point as a Vector subclass with optional
parent face tracking.
"""

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
    """3D point, subclass of Vector with optional parent face tracking."""

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

    def addRuler(self, other: object) -> None:
        """Store a ruler reference for this point (e.g., for measurement UI).

        Args:
            other: Ruler reference to store.
        """
        self.ruler = other
