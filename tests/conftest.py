"""Pytest configuration and path setup for meshTools binding tests.

When the package is installed (pip install), meshTools and its extensions
are found from site-packages. When running from a development tree, this
conftest adds the build output (extensions) and python/ to sys.path so
extensions and the meshTools package are found. Run from repo root after
building; optionally set MESHTOOLS_BUILD_DIR.
"""

import sys
from pathlib import Path

# Repo root: conftest is in tests/
_repo_root = Path(__file__).resolve().parent.parent

# Prefer explicit build dir (e.g. CI or custom build)
_build_dir = Path(__file__).resolve().parent.parent / "build"
if "MESHTOOLS_BUILD_DIR" in __import__("os").environ:
    _build_dir = Path(__import__("os").environ["MESHTOOLS_BUILD_DIR"])

# Where extensions live: install dir (scripts), per-target dirs, or Debug/Release
_candidates = [
    _build_dir / "scripts",
    _build_dir / "bindings" / "geometry_mesh" / "Debug",
    _build_dir / "bindings" / "geometry_mesh" / "Release",
    _build_dir / "bindings" / "geometry_mesh",
    _build_dir / "bindings" / "bezier" / "Debug",
    _build_dir / "bindings" / "bezier" / "Release",
    _build_dir / "bindings" / "bezier",
]
for _ext_dir in _candidates:
    if _ext_dir.exists():
        _s = str(_ext_dir.resolve())
        if _s not in sys.path:
            sys.path.insert(0, _s)

# Package location when not installed (development)
_python_dir = _repo_root / "python"
if _python_dir.exists():
    _s = str(_python_dir.resolve())
    if _s not in sys.path:
        sys.path.insert(0, _s)
