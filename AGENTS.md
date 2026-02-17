# AGENTS.md

Guidance for coding agents working in this repository.

## Tooling policy

- Do not use `pip` directly in this repository.
- Always use `uv` commands (`uv pip ...`, `uv run ...`) for installs and Python tooling.

## Purpose

Use this file as the default workflow reference after making changes:

1. Build/install the project (so native extensions are available).
2. Run tests.
3. Run formatting checks (and apply formatting when needed).

All commands below come from the repository `README.md` and existing scripts.

## Requirements

- Python 3.12+
- CMake 3.18+
- `clang-format` on PATH (for C++ formatting)

## Build

Preferred (installable) workflows:

```bash
uv pip install .
# editable install:
uv pip install -e .
```

Standalone CMake build (without installing):

```bash
cmake -S . -B build
cmake --build build
```

Notes:

- The build produces `_geometry`, `_mesh`, and `_bezier` extension modules.
- When tests are run from the repo, `tests/conftest.py` helps discover build outputs.
- Use `MESHTOOLS_BUILD_DIR` to point tests at a non-default build directory.

## Run tests

Python tests (from repo root):

```bash
uv run pytest tests/ -v
```

C++ unit tests (GoogleTest via CTest, after building):

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
```

Windows multi-config example (from README):

```bash
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

## Formatting

C++ formatting is defined for files under `src/` and `bindings/`:

- Linux/macOS/Git Bash:

```bash
./scripts/format.sh
```

- Windows PowerShell:

```powershell
.\scripts\format.ps1
```

Python formatting and lint:

- To **check** only (same as CI): `uv run ruff format --check .` and `uv run ruff check .`
- To **fix** formatting: `uv run ruff format .` then run `uv run ruff check .`

```bash
uv run ruff format --check .
uv run ruff check .
# If format check fails: uv run ruff format . then re-run checks.
```

## Agent checklist after code changes

1. If you changed C++ in `src/` or `bindings/`, run the formatting script.
2. Ensure the project builds (installable or standalone CMake path).
3. Run relevant tests (at minimum `uv run pytest tests/ -v`; include `ctest` for C++ changes).
4. Run Python format/lint: `uv run ruff format --check .` and `uv run ruff check .`; if format check fails, run `uv run ruff format .` and re-check.
5. Review diffs and confirm generated formatting changes are included in your commit.
