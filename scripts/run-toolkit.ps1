# Windows Automation Toolkit - PowerShell Launcher
# Downloads Python if needed, then runs the toolkit

param(
    [switch]$InstallPython,
    [switch]$NoPrompt
)

$ErrorActionPreference = "Stop"
# Repository URL - update if forked
$ToolkitRepo = "https://github.com/Drakaniia/qwenzy"
$PythonInstaller = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
$TempDir = $env:TEMP
$PythonExe = "python.exe"

function Write-Header {
    param([string]$Title)
    Clear-Host
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  $Title" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host
}

function Test-PythonInstalled {
    try {
        $null = Get-Command python -ErrorAction Stop
        $version = python --version
        return $true
    } catch {
        return $false
    }
}

function Install-Python {
    Write-Host "Downloading Python installer..." -ForegroundColor Yellow
    $InstallerPath = Join-Path $TempDir "python-installer.exe"
    Invoke-WebRequest -Uri $PythonInstaller -OutFile $InstallerPath
    
    Write-Host "Installing Python silently..." -ForegroundColor Yellow
    Start-Process -FilePath $InstallerPath -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1" -Wait
    
    Remove-Item $InstallerPath -Force
    Write-Host "Python installed successfully!" -ForegroundColor Green
}

function Clone-Toolkit {
    $ToolkitPath = Join-Path $env:USERPROFILE "windows-automation-toolkit"
    
    if (Test-Path $ToolkitPath) {
        Write-Host "Toolkit already exists. Updating..." -ForegroundColor Yellow
        Set-Location $ToolkitPath
        git pull
    } else {
        Write-Host "Cloning toolkit repository..." -ForegroundColor Yellow
        git clone $ToolkitRepo $ToolkitPath
        Set-Location $ToolkitPath
    }
    
    return $ToolkitPath
}

function Install-Requirements {
    Write-Host "Installing Python requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "Requirements installed!" -ForegroundColor Green
}

# Main execution
Write-Header "Windows Automation Toolkit Launcher"

if (-not (Test-PythonInstalled)) {
    Write-Host "Python is not installed!" -ForegroundColor Red
    
    if ($InstallPython -or $NoPrompt) {
        Install-Python
    } else {
        $response = Read-Host "Install Python now? (y/n)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            Install-Python
        } else {
            Write-Host "Cannot continue without Python. Exiting." -ForegroundColor Red
            exit 1
        }
    }
}

$ToolkitPath = Clone-Toolkit
Set-Location $ToolkitPath
Install-Requirements

Write-Host "`nStarting Windows Automation Toolkit..." -ForegroundColor Green
python main.py
