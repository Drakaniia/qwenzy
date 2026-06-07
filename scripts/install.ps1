# Windows Toolkit - One-Line Launcher
# Usage: iwr https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install.ps1 | iex

$ErrorActionPreference = "Stop"
$ReleaseUrl = "https://github.com/Drakaniia/qwenzy/releases/latest/download/WindowsToolkit.zip"
$InstallDir = Join-Path $env:TEMP "WindowsToolkit"
$ZipPath = Join-Path $InstallDir "WindowsToolkit.zip"
$ExePath = Join-Path $InstallDir "WindowsToolkit.exe"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Windows Toolkit - Downloading..." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host

Write-Host "Downloading from GitHub Releases..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
Invoke-WebRequest -Uri $ReleaseUrl -OutFile $ZipPath -UseBasicParsing

Write-Host "Extracting..." -ForegroundColor Yellow
Expand-Archive -Path $ZipPath -DestinationPath $InstallDir -Force

# Clean up zip (ignore errors if file is in use)
try { Remove-Item $ZipPath -Force -ErrorAction SilentlyContinue } catch {}

if (-not (Test-Path -Path $ExePath)) {
    throw "Expected executable not found after extraction: $ExePath"
}

Write-Host "Launching Windows Toolkit..." -ForegroundColor Green
Write-Host

Start-Process -FilePath $ExePath -Verb RunAs
