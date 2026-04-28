# Download and run the standalone executable
# One-liner: iwr https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/run-exe.ps1 | iex

param([switch]$NoPrompt)

$ErrorActionPreference = "Stop"
$ReleaseUrl = "https://api.github.com/repos/Drakaniia/qwenzy/releases/latest"
$TempDir = $env:TEMP
$ExePath = Join-Path $TempDir "WindowsAutomationToolkit.exe"
$ZipPath = Join-Path $TempDir "WindowsToolkit.zip"

function Write-Header {
    param([string]$Title)
    Clear-Host
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host
}

function Get-LatestRelease {
    try {
        $response = Invoke-RestMethod -Uri $ReleaseUrl -UseBasicParsing
        return $response
    } catch {
        Write-Host "Failed to fetch latest release: $_" -ForegroundColor Red
        exit 1
    }
}

function Download-Executable {
    param([string]$DownloadUrl)

    Write-Host "Downloading WindowsAutomationToolkit.exe..." -ForegroundColor Yellow
    Write-Host "From: $DownloadUrl" -ForegroundColor Gray

    try {
        Invoke-WebRequest -Uri $DownloadUrl -OutFile $ExePath -UseBasicParsing
        Write-Host "Download complete!" -ForegroundColor Green
    } catch {
        Write-Host "Download failed: $_" -ForegroundColor Red
        exit 1
    }
}

function Download-And-Extract-Zip {
    param([string]$DownloadUrl)

    Write-Host "Downloading WindowsToolkit.zip..." -ForegroundColor Yellow
    Write-Host "From: $DownloadUrl" -ForegroundColor Gray

    try {
        Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipPath -UseBasicParsing
        Write-Host "Download complete! Extracting..." -ForegroundColor Green
        
        Expand-Archive -Path $ZipPath -DestinationPath $TempDir -Force
        Remove-Item $ZipPath -Force
        
        Write-Host "Extraction complete!" -ForegroundColor Green
    } catch {
        Write-Host "Download/extract failed: $_" -ForegroundColor Red
        exit 1
    }
}

function Confirm-Run {
    if ($NoPrompt) { return $true }

    $response = Read-Host "Run Windows Toolkit now? (y/n)"
    return ($response -eq "y" -or $response -eq "Y")
}

# Main execution
Write-Header "Windows Toolkit - Executable Launcher"

$release = Get-LatestRelease

# Try to find .exe first, then .zip
$asset = $release.assets | Where-Object { $_.name -eq "WindowsAutomationToolkit.exe" }
$useZip = $false

if (-not $asset) {
    $asset = $release.assets | Where-Object { $_.name -eq "WindowsToolkit.zip" }
    $useZip = $true
}

if (-not $asset) {
    Write-Host "No WindowsAutomationToolkit.exe or WindowsAutomationToolkit.zip found in latest release!" -ForegroundColor Red
    Write-Host "Latest release: $($release.tag_name)" -ForegroundColor Yellow
    Write-Host "Check releases at: https://github.com/Drakaniia/qwenzy/releases" -ForegroundColor Yellow
    exit 1
}

Write-Host "Latest version: $($release.tag_name)" -ForegroundColor Cyan
Write-Host "Published: $($release.published_at)" -ForegroundColor Gray
Write-Host

if ($useZip) {
    Download-And-Extract-Zip $asset.browser_download_url
} else {
    Download-Executable $asset.browser_download_url
}

if (Confirm-Run) {
    Write-Host "`nLaunching Windows Toolkit..." -ForegroundColor Green
    Start-Process -FilePath $ExePath -Wait
} else {
    Write-Host "`nExecutable saved to: $ExePath" -ForegroundColor Yellow
    Write-Host "Run it manually or create a shortcut." -ForegroundColor Gray
}
