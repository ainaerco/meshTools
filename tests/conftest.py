"""Pytest configuration and path setup for meshTools binding tests.

Ensures the build output (extensions) and Python package are on sys.path.
Run from repo root after building; optionally set MESHTOOLS_BUILD_DIR.
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
    _build_dir / "module" / "Debug",
    _build_dir / "module" / "Release",
    _build_dir / "module",
    _build_dir / "bezierModule" / "Debug",
    _build_dir / "bezierModule" / "Release",
    _build_dir / "bezierModule",
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
