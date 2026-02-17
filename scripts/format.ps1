# Format C++ sources with clang-format using .clang-format in repo root.
# Run from repo root: .\scripts\format.ps1
# Or from anywhere: & ".\path\to\meshTools\scripts\format.ps1"
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$files = Get-ChildItem -Path src, bindings -Recurse -Include "*.cpp", "*.h" -ErrorAction SilentlyContinue
if (-not $files) {
    Write-Host "No C++ sources found under src/ or bindings/."
    exit 0
}
foreach ($f in $files) {
    & clang-format -i $f.FullName
    Write-Host "Formatted: $($f.FullName)"
}
Write-Host "Done."
