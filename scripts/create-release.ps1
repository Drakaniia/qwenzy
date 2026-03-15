# Create GitHub Release and Upload Executable
# Run this after building the .exe

$ErrorActionPreference = "Stop"

$RepoOwner = "Drakaniia"
$RepoName = "qwenzy"
$Version = "v2.1.0"
$ExePath = Join-Path $PSScriptRoot "..\dist\WindowsToolkit.exe"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Creating GitHub Release $Version" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host

# Check if executable exists
if (-not (Test-Path $ExePath)) {
    Write-Host "Error: WindowsToolkit.exe not found!" -ForegroundColor Red
    Write-Host "Run build-exe.ps1 first." -ForegroundColor Yellow
    exit 1
}

$ExeSize = (Get-Item $ExePath).Length / 1MB
Write-Host "Executable found: {0:F2} MB" -ForegroundColor Green -ArgumentList $ExeSize
Write-Host

Write-Host "Creating release on GitHub..." -ForegroundColor Yellow
Write-Host
Write-Host "IMPORTANT: You need to create the release manually:" -ForegroundColor Yellow
Write-Host "1. Go to: https://github.com/$RepoOwner/$RepoName/releases/new" -ForegroundColor White
Write-Host "2. Tag version: $Version" -ForegroundColor White
Write-Host "3. Release title: Windows Toolkit $Version" -ForegroundColor White
Write-Host "4. Upload: $ExePath" -ForegroundColor White
Write-Host
Write-Host "Opening releases page..." -ForegroundColor Green

# Open the releases page
Start-Process "https://github.com/$RepoOwner/$RepoName/releases/new"

Write-Host
Write-Host "After uploading:" -ForegroundColor Yellow
Write-Host "- The run-exe.ps1 script will work automatically" -ForegroundColor White
Write-Host "- Users can download from: https://github.com/$RepoOwner/$RepoName/releases" -ForegroundColor White
