"""meshTools: 3D mesh geometry library with C++ bindings and pure-Python layer."""

# Expose C extension modules for code that uses them directly (e.g. meshTools._mesh).
# Prefer package-internal (pip install); fall back to top-level (dev with build on path).
try:
    from . import _geometry
except ImportError:
    try:
        import _geometry
    except ImportError:
        _geometry = None  # type: ignore[assignment]

try:
    from . import _mesh
except ImportError:
    try:
        import _mesh
    except ImportError:
        _mesh = None  # type: ignore[assignment]

try:
    from . import _bezier
except ImportError:
    try:
        import _bezier
    except ImportError:
        _bezier = None  # type: ignore[assignment]

# Re-export common public API from geometry and mesh
from .geometry import (
    BBox,
    EPSILON,
    OBBox,
    Point,
    Polygon,
    Ray,
    Transform,
    Vector,
    epsilonTest,
    fit,
    getBarycentric,
    interpolateBezier,
    interpolateCatmullRom,
    lerp,
    pointInPoly,
    solveCubic,
    sortedVectorArray,
)
from .mesh import Mesh, kGeotype, kResult

__all__ = [
    # C extensions (may be None if not built)
    "_geometry",
    "_mesh",
    "_bezier",
    # Geometry
    "BBox",
    "EPSILON",
    "OBBox",
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
    "pointInPoly",
    "solveCubic",
    "sortedVectorArray",
    # Mesh
    "Mesh",
    "kGeotype",
    "kResult",
]
