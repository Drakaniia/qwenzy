# Windows Toolkit - One-Line Launcher
# Usage: iwr https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install.ps1 | iex

$ErrorActionPreference = "Stop"
$ReleaseUrl = "https://github.com/Drakaniia/qwenzy/releases/latest/download/WindowsToolkit.zip"
$TempDir = $env:TEMP
$ZipPath = Join-Path $TempDir "WindowsToolkit.zip"
$ExePath = Join-Path $TempDir "WindowsAutomationToolkit.exe"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Windows Toolkit - Downloading..." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host

Write-Host "Downloading from GitHub Releases..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $ReleaseUrl -OutFile $ZipPath -UseBasicParsing

Write-Host "Extracting..." -ForegroundColor Yellow
Expand-Archive -Path $ZipPath -DestinationPath $TempDir -Force

# Clean up zip (ignore errors if file is in use)
try { Remove-Item $ZipPath -Force -ErrorAction SilentlyContinue } catch {}

Write-Host "Launching Windows Toolkit..." -ForegroundColor Green
Write-Host

Start-Process -FilePath $ExePath
