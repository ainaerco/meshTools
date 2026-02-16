# meshTools

A 3D mesh geometry library providing both C++ core implementations and Python bindings, with optional integration for Autodesk Maya.

## Overview

meshTools is a collection of geometric algorithms and data structures for 3D mesh processing. It exposes a C++ core via [nanobind](https://github.com/wjakob/nanobind) extension modules (Python 3.12+), and includes a pure-Python mesh layer on top. Maya-specific utilities allow the library to be used directly inside Autodesk Maya scripts.

## Features

- **Vector/BBox math** — Vector3, bounding box (AABB and OBB), ray casting, transforms, polygon utilities
- **Mesh data structures** — Vertex, Edge, Face topology with normal computation and bounding box support
- **Curve interpolation** — Bezier, Lagrange, and Catmull-Rom spline evaluation
- **Convex Hull** — Incremental 3D convex hull algorithm (O'Rourke method)
- **Delaunay triangulation** — 2D Delaunay triangulation
- **Polygon triangulation** — Ear-clipping triangulation for arbitrary polygons
- **Noise** — Perlin-style value noise (2D and 3D)
- **Maya integration** — `MayaMesh` class, oriented bounding box tool, tile scatter, tube deformer

## Repository Structure

```
meshTools/
├── CMakeLists.txt          # Top-level CMake build
├── geometry/               # C++ geometry math (Vector, BBox, List, math utils)
├── mesh/                   # C++ mesh topology (Vert, Edge, Face, Mesh)
├── bezier/                 # C++ curve classes (Bezier, Lagrange, Spline)
├── bezierModule/           # nanobind bindings for bezier curves -> _bezier
├── module/                 # nanobind bindings for geometry + mesh -> _geometry, _mesh
└── python/
    ├── CMakeLists.txt
    ├── meshTools/          # Python package
    │   ├── __init__.py
    │   ├── geometry.py     # Wraps _geometry C++ module; Vector, BBox, Ray, Transform, ...
    │   ├── mesh.py         # Pure-Python Mesh class (verts, faces, edges, normals, uvs)
    │   ├── chull.py        # 3D convex hull (incremental algorithm)
    │   ├── delaunay.py     # 2D Delaunay triangulation
    │   ├── triangulate.py  # Ear-clipping polygon triangulation
    │   ├── noise.py        # Perlin-style noise
    │   ├── noise_tabs.py   # Noise lookup tables
    │   └── lists.py        # List/enumeration helpers
    ├── mesh_maya.py        # MayaMesh — Maya-aware Mesh subclass
    ├── obb.py              # Oriented bounding box helper for Maya selections
    ├── mesh_maya_scatter.py# Tile-scatter mesh faces in Maya
    ├── mesh_maya_tube.py   # Tube mesh generator for Maya
    ├── tubeDeformer.py     # Tube deformer script
    ├── convexHull.py       # Standalone convex hull script
    ├── flowLoop.py         # Flow loop utility
    └── module_geometry_tests.py  # Geometry module tests
```

## Dependencies

| Dependency | Notes |
|---|---|
| CMake >= 3.18 | Build system (nanobind fetched via FetchContent) |
| Python 3.12+ | Extension modules target Python 3.12 |
| nanobind | C++/Python bridge (fetched automatically) |
| Autodesk Maya | Required only for `mesh_maya*.py` and `obb.py` |

## Building

Requires **CMake 3.18+** and **Python 3.12** (development headers). nanobind is fetched automatically via FetchContent.

```bash
mkdir build && cd build
cmake ..   # optionally: -DPython_ROOT_DIR=/path/to/python3.12
cmake --build .
```

On Windows, use a generator such as `-G "Visual Studio 17 2022" -A x64` if not using Ninja.

The build produces Python extension modules (`.so` on Linux, `.pyd` on Windows) that are imported by the Python package:

- `_geometry` — geometry math (Vector, BBox, Ray, Transform, lerp, fit, solveCubic, …)
- `_mesh` — Mesh/Vert topology classes
- `_bezier` — Bezier/Lagrange/Spline curve evaluation

### Platform notes

- **Linux** — compiled with `-fPIC`
- **macOS** — C++11 enabled for OS X 10.9+
- **Windows** — produces `.pyd` modules; `PLATFORM_WINDOWS` preprocessor define is set

## Python API

### Geometry primitives (`meshTools.geometry`)

```python
from meshTools.geometry import Vector, BBox, Ray, Transform, lerp, fit

v = Vector(1.0, 0.0, 0.0)
bbox = BBox()
bbox.obbFromPointSet([Vector(0,0,0), Vector(1,1,1), ...])

t = Transform()
euler = t.getEuler()
```

### Mesh (`meshTools.mesh`)

```python
from meshTools.mesh import Mesh

m = Mesh()
# m.vertices — list of Vector
# m.faces    — list of face index lists
# m.normals  — per-vertex normals
# m.edges    — edge list (populated on demand)
```

### Convex Hull (`meshTools.chull`)

```python
from meshTools.chull import Hull

points = [Vector(x, y, z), ...]
hull = Hull(points)
faces, vertices = hull.exportHull()
```

### Noise (`meshTools.noise`)

```python
from meshTools.noise import Noise

n = Noise()
value = n.noise(x, y)        # 2D
value = n.noise(x, y, z)     # 3D, returns float in [-1, 1]
```

### Curves (`_bezier` C++ module)

```python
from _bezier import Bezier, Lagrange, Spline

b = Bezier([0.0, 0.5, 1.0])
interpolated = b.interpolate(100)   # 100 evenly-spaced samples
```

### Maya integration

```python
# Inside a Maya Python session
import meshTools.mesh as mesh
from mesh_maya import MayaMesh
import maya.OpenMaya as OpenMaya

dag = ...  # MDagPath to a mesh
m = MayaMesh(dag=dag, vertices=True, faces=True, normals=True)
```

## Math utilities (`_geometry` C++ module)

| Function | Description |
|---|---|
| `lerp(t, a, b)` | Linear interpolation |
| `fit(p, oldmin, oldmax, newmin, newmax)` | Range remap |
| `solveCubic(a, b, c, d)` | Roots of cubic polynomial |
| `epsilonTest(value, test, eps)` | Floating-point equality test |
| `pointInPoly(point, poly)` | 2D point-in-polygon test |

## License

See [LICENSE](LICENSE) for details.
