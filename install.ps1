Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$Python = Get-Command py -ErrorAction SilentlyContinue
if (-not $Python) {
    $Python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $Python) {
    $Python = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $Python) {
    throw "Python is required but was not found."
}

if ($args -notcontains "--dry-run") {
    Write-Host "Tip: run .\install.ps1 --dry-run to preview changes before installing."
}

& $Python.Source scripts\install_codex_plugin.py @args
if ($LASTEXITCODE -ne 0) {
    throw "Install failed with exit code $LASTEXITCODE."
}
