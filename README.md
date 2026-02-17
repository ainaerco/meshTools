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
├── src/                    # C++ libraries only
│   ├── geometry/           # Vector, BBox, Ray, Transform, Polygon, math (snake_case filenames)
│   ├── mesh/               # Mesh topology (Vert, Edge, Face)
│   └── bezier/             # Bezier, Lagrange, Spline curves
├── bindings/               # Python extension bindings only
│   ├── geometry_mesh/      # _geometry, _mesh (nanobind)
│   └── bezier/             # _bezier (nanobind)
└── python/
    ├── CMakeLists.txt
    └── meshTools/          # Python package
        ├── __init__.py     # Core API; no Maya dependency
        ├── geometry.py     # Wraps _geometry; Vector, BBox, Ray, Transform, ...
        ├── mesh.py         # Pure-Python Mesh class
        ├── chull.py        # 3D convex hull
        ├── delaunay.py     # 2D Delaunay triangulation
        ├── triangulate.py  # Ear-clipping polygon triangulation
        ├── noise.py        # Perlin-style noise
        ├── noise_tabs.py   # Noise lookup tables
        ├── lists.py        # List/enumeration helpers
        └── maya/           # Optional: use only inside Autodesk Maya
            ├── __init__.py # Re-exports MayaMesh, kGeotype, MayaTube
            ├── mesh.py     # MayaMesh — Maya-aware Mesh subclass
            ├── tube.py     # MayaTube tube mesh generator
            ├── scatter.py  # Tile-scatter mesh faces
            ├── obb.py      # Oriented bounding box helper
            ├── tube_deformer.py
            ├── convex_hull.py
            └── flow_loop.py # Flow loop Maya command
```

## Dependencies

| Dependency | Notes |
|---|---|
| CMake >= 3.18 | Build system (nanobind fetched via FetchContent) |
| Python 3.12+ | Extension modules target Python 3.12 |
| nanobind | C++/Python bridge (fetched automatically) |
| Autodesk Maya | Required only for the optional `meshTools.maya` subpackage |

## Building

Requires **CMake 3.18+** and **Python 3.12** (development headers). nanobind is fetched automatically.

### Installable (recommended)

Install the package and its C++ extensions into your environment:

```bash
pip install .
# or editable install:
pip install -e .
# or with uv:
uv pip install -e .
```

This uses [scikit-build-core](https://scikit-build-core.readthedocs.io/) to run CMake, build the extensions, and install the `meshTools` package (including `_geometry`, `_mesh`, `_bezier`) into your Python environment. No need to set `MESHTOOLS_BUILD_DIR` when running tests after install.

### Standalone CMake

Build without installing; extensions end up in `build/scripts` (or per-target dirs). Useful for development.

```bash
mkdir build && cd build
cmake ..   # optionally: -DPython_ROOT_DIR=/path/to/python3.12
cmake --build .
```

On Windows, use a generator such as `-G "Visual Studio 17 2022" -A x64` if not using Ninja.

When running tests from the repo without installing, `tests/conftest.py` adds the build output and `python/` to `sys.path` so the package and extensions are found.

The build produces Python extension modules (`.so` on Linux, `.pyd` on Windows) that are imported by the Python package:

- `_geometry` — geometry math (Vector, BBox, Ray, Transform, lerp, fit, solveCubic, …)
- `_mesh` — Mesh/Vert topology classes
- `_bezier` — Bezier/Lagrange/Spline curve evaluation

### Platform notes

- **Linux** — compiled with `-fPIC`
- **macOS** — C++11 enabled for OS X 10.9+
- **Windows** — produces `.pyd` modules; `PLATFORM_WINDOWS` preprocessor define is set

## Testing

Python tests for the C++ bindings live in `tests/`. They require the extension modules to be built first (see [Building](#building)).

From the repository root:

```bash
uv run pytest tests/ -v
```

or, with pytest already installed:

```bash
pytest tests/ -v
```

The test suite uses `tests/conftest.py` to add the build output to `sys.path`, so extensions are found from `build/scripts`, `build/bindings/geometry_mesh`, or `build/bindings/bezier`. To use a custom build directory, set the environment variable `MESHTOOLS_BUILD_DIR`.

| Test module | Coverage |
|---|---|
| `test_bindings_geometry.py` | Vector, BBox, Ray, Transform, Polygon, and math functions (`lerp`, `fit`, `pointInPoly`, `solveCubic`, etc.) via `meshTools.geometry` |
| `test_bindings_mesh.py` | C++ `_mesh` module: Mesh, Vert |
| `test_bindings_bezier.py` | C++ `_bezier` module: Bezier, Lagrange, Spline |

If an extension is not built or not on the path, its tests are skipped automatically.

### C++ unit tests (GoogleTest)

C++ unit tests live in `tests/cpp/` and are run with `ctest` after a successful CMake build.

**Visual Studio generator (multi-config):**

```bash
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
ctest --test-dir build -C Release
```

**Single-config generators (Ninja / Makefiles):**

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build
```

**Useful options:**

```bash
# show failing test output
ctest --test-dir build -C Release --output-on-failure

# run a subset by regex
ctest --test-dir build -C Release -R VectorTest
```

You can also run the test executables directly (paths depend on generator/config), e.g.
`build/tests/cpp/Release/geometry_tests.exe` and `build/tests/cpp/Release/bezier_tests.exe` on Windows.

## Code formatting (C++)

C++ under `src/` and `bindings/` is formatted with [clang-format](https://clang.llvm.org/docs/ClangFormat.html) using customized LLVM style (see `.clang-format`).

- **Windows (PowerShell):** from the repo root run  
  `.\scripts\format.ps1`
- **Linux / macOS / Git Bash:**  
  `./scripts/format.sh`

Requires `clang-format` on your PATH.

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

### Maya integration (optional)

The `meshTools.maya` subpackage is for use only inside Autodesk Maya. The core `meshTools` package has no Maya dependency.

```python
# Inside a Maya Python session
from meshTools.maya import MayaMesh  # or: from meshTools.maya.mesh import MayaMesh
import maya.OpenMaya as OpenMaya

dag = ...  # MDagPath to a mesh
m = MayaMesh(dag=dag, vertices=1, faces=1, normals=1)
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
