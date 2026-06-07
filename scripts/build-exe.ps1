# Build standalone executable using PyInstaller
# Run this after installing dependencies: pip install -r requirements.txt

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

# Check if PyInstaller is installed
try {
    $null = Get-Command pyinstaller -ErrorAction Stop
} catch {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller --quiet
}

# Create dist directory if it doesn't exist
$DistDir = Join-Path $PSScriptRoot "..\dist"
if (-not (Test-Path $DistDir)) {
    New-Item -ItemType Directory -Path $DistDir | Out-Null
}

Write-Host "Building executable..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

# Build with PyInstaller
# Note: No --windowed flag - console is needed for user input
pyinstaller `
    --onefile `
    --name "WindowsToolkit" `
    --icon=NONE `
    --add-data "src;src" `
    --hidden-import=requests `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================================" -ForegroundColor Green
    Write-Host "  Build Successful!" -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
    Write-Host
    Write-Host "Executable created: dist\WindowsToolkit.exe" -ForegroundColor Cyan
    Write-Host
    Write-Host "You can now:" -ForegroundColor Yellow
    Write-Host "  1. Distribute the .exe file directly" -ForegroundColor White
    Write-Host "  2. Upload to GitHub Releases" -ForegroundColor White
    Write-Host "  3. Test by running: .\dist\WindowsToolkit.exe" -ForegroundColor White
    Write-Host
} else {
    Write-Host "`nBuild failed! Check the error messages above." -ForegroundColor Red
    exit 1
}
