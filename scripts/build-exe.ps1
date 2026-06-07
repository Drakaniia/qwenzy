# Build standalone executable using PyInstaller from an isolated build venv.
# This avoids accidentally bundling unrelated packages from the user's global
# Python environment.

param(
    [switch]$CleanVenv
)

$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Building Windows Automation Toolkit Executable" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host

# Check if in correct directory
if (-not (Test-Path "main.py")) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VenvDir = Join-Path $RootDir ".build-venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

if ($CleanVenv -and (Test-Path $VenvDir)) {
    $ResolvedVenv = (Resolve-Path $VenvDir).Path
    if (-not $ResolvedVenv.StartsWith($RootDir, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove unexpected venv path: $ResolvedVenv"
    }

    Write-Host "Removing existing build virtualenv..." -ForegroundColor Yellow
    Remove-Item -LiteralPath $ResolvedVenv -Recurse -Force
}

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating isolated build virtualenv..." -ForegroundColor Yellow
    python -m venv $VenvDir
}

Write-Host "Installing build dependencies in isolated virtualenv..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip --quiet
& $VenvPython -m pip install -r (Join-Path $RootDir "requirements.txt") --quiet

Write-Host "Building executable..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

& $VenvPython (Join-Path $RootDir "build\build-executable.py")

if ($LASTEXITCODE -eq 0) {
    $ExePath = Join-Path $RootDir "launcher\WindowsToolkit.exe"
    $ZipPath = Join-Path $RootDir "launcher\WindowsToolkit.zip"

    Write-Host "Creating zip archive..." -ForegroundColor Yellow
    Compress-Archive -Path $ExePath -DestinationPath $ZipPath -Force

    $ExeSize = (Get-Item $ExePath).Length / 1MB
    $ZipSize = (Get-Item $ZipPath).Length / 1MB

    Write-Host "`n========================================================" -ForegroundColor Green
    Write-Host "  Build Successful!" -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
    Write-Host
    Write-Host ("Executable created: launcher\WindowsToolkit.exe ({0:F2} MB)" -f $ExeSize) -ForegroundColor Cyan
    Write-Host ("Zip created:        launcher\WindowsToolkit.zip ({0:F2} MB)" -f $ZipSize) -ForegroundColor Cyan
    Write-Host
    Write-Host "You can now:" -ForegroundColor Yellow
    Write-Host "  1. Upload launcher\WindowsToolkit.zip to GitHub Releases" -ForegroundColor White
    Write-Host "  2. Distribute launcher\WindowsToolkit.exe directly" -ForegroundColor White
    Write-Host "  3. Test by running: .\launcher\WindowsToolkit.exe" -ForegroundColor White
    Write-Host
} else {
    Write-Host "`nBuild failed! Check the error messages above." -ForegroundColor Red
    exit 1
}
