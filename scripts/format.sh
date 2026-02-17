#!/usr/bin/env bash
# Format C++ sources with clang-format (LLVM style, 4 spaces). Run from repo root.
# On Windows use: .\scripts\format.ps1
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
find src bindings -type f \( -name '*.cpp' -o -name '*.h' \) -exec clang-format -i {} +
echo "Formatted C++ sources."
