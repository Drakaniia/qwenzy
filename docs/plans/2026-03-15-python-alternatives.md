# Python Alternatives Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide multiple installation options for users without Python, including PowerShell script, standalone executable, and MSIX installer.

**Architecture:** Create parallel entry points that wrap the existing Python functionality: (1) Pure PowerShell script for basic operations, (2) PyInstaller-frozen executable with embedded Python, (3) ClickOnce/MSIX installer package.

**Tech Stack:** PowerShell 5.1+, PyInstaller, Inno Setup, Windows Package Manager (winget), MSIX Packaging Tool

---

## File Structure

**New Files:**
- `scripts/install-toolkit.ps1` - PowerShell installer that downloads and runs toolkit
- `scripts/run-toolkit.ps1` - Pure PowerShell wrapper script
- `build/build-executable.py` - PyInstaller build configuration
- `build/create-installer.iss` - Inno Setup installer script
- `docs/INSTALLATION.md` - Installation alternatives documentation
- `launcher/toolkit-launcher.exe` - Compiled standalone executable (gitignored)

**Modified Files:**
- `Readme.md` - Add installation alternatives section
- `requirements.txt` - Add pyinstaller for building

---

### Task 1: PowerShell-Only Alternative

**Files:**
- Create: `scripts/run-toolkit.ps1`
- Create: `scripts/install-toolkit.ps1`
- Test: Manual testing on Windows without Python

**Rationale:** PowerShell can execute most Windows automation tasks directly without Python. This provides immediate accessibility.

- [ ] **Step 1: Create PowerShell wrapper script**

```powershell
# scripts/run-toolkit.ps1
# Windows Automation Toolkit - PowerShell Launcher
# Downloads Python if needed, then runs the toolkit

param(
    [switch]$InstallPython,
    [switch]$NoPrompt
)

$ErrorActionPreference = "Stop"
$ToolkitRepo = "https://github.com/yourusername/windows-automation-toolkit"
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
```

- [ ] **Step 2: Create one-line installer script**

```powershell
# scripts/install-toolkit.ps1
# One-line installer: iwr https://yourdomain.com/install.ps1 | iex

param([switch]$NoPrompt)

$ScriptUrl = "https://raw.githubusercontent.com/yourusername/windows-automation-toolkit/main/scripts/run-toolkit.ps1"
$TempScript = Join-Path $env:TEMP "toolkit-launcher.ps1"

Write-Host "Downloading toolkit launcher..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $ScriptUrl -OutFile $TempScript

Write-Host "Starting toolkit..." -ForegroundColor Green
& $TempScript -NoPrompt:$NoPrompt
```

- [ ] **Step 3: Test PowerShell scripts manually**

Run on Windows machine without Python:
```powershell
# Test the installer
powershell -ExecutionPolicy Bypass -File .\scripts\install-toolkit.ps1

# Test the launcher
powershell -ExecutionPolicy Bypass -File .\scripts\run-toolkit.ps1
```

Expected: Downloads Python if needed, clones repo, installs requirements, runs toolkit

- [ ] **Step 4: Commit**

```bash
git add scripts/run-toolkit.ps1 scripts/install-toolkit.ps1
git commit -m "feat: add PowerShell launcher scripts for Python-less installation"
```

---

### Task 2: Standalone Executable with PyInstaller

**Files:**
- Create: `build/build-executable.py`
- Create: `build/toolkit.spec`
- Modify: `requirements.txt`
- Test: `launcher/toolkit.exe` on clean Windows VM

**Rationale:** PyInstaller bundles Python interpreter and all dependencies into a single .exe file.

- [ ] **Step 1: Add PyInstaller to requirements**

```txt
# requirements.txt
requests>=2.25.0
pyinstaller>=6.0.0
```

- [ ] **Step 2: Create PyInstaller spec file**

```python
# build/toolkit.spec
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../src', 'src'),
        ('../src/config', 'src/config'),
        ('../src/modules', 'src/modules'),
        ('../src/utils', 'src/utils'),
    ],
    hiddenimports=[
        'src.config.settings',
        'src.utils.system',
        'src.modules.debloat',
        'src.modules.settings',
        'src.modules.power',
        'src.modules.installer',
        'src.modules.ai_tools',
        'src.modules.autohotkey',
    ] + collect_submodules('src'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WindowsAutomationToolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/toolkit.ico',  # Optional: add icon later
)
```

- [ ] **Step 3: Create build script**

```python
# build/build-executable.py
#!/usr/bin/env python3
"""Build standalone executable using PyInstaller"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the standalone executable"""
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(root_dir, 'launcher')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean previous builds
    build_dir = os.path.join(script_dir, 'build')
    dist_dir = os.path.join(script_dir, 'dist')
    
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    # Run PyInstaller
    spec_file = os.path.join(script_dir, 'toolkit.spec')
    
    print("Building executable with PyInstaller...")
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--distpath', output_dir,
        '--workpath', build_dir,
        '--specpath', script_dir,
        spec_file
    ], check=True)
    
    print(f"\n✓ Executable built successfully!")
    print(f"  Location: {os.path.join(output_dir, 'WindowsAutomationToolkit.exe')}")
    print(f"  Size: {os.path.getsize(os.path.join(output_dir, 'WindowsAutomationToolkit.exe')) / (1024*1024):.1f} MB")

if __name__ == '__main__':
    build_executable()
```

- [ ] **Step 4: Build and test executable**

```bash
# Build the executable
python build/build-executable.py

# Test on clean Windows VM (no Python installed)
.\launcher\WindowsAutomationToolkit.exe
```

Expected: Runs toolkit without requiring Python installation

- [ ] **Step 5: Add launcher to .gitignore**

```txt
# .gitignore
...
# Built executables
launcher/*.exe
launcher/*.pdb
build/
dist/
```

- [ ] **Step 6: Commit**

```bash
git add requirements.txt build/toolkit.spec build/build-executable.py .gitignore
git commit -m "feat: add PyInstaller build for standalone executable"
```

---

### Task 3: Inno Setup Installer

**Files:**
- Create: `build/create-installer.iss`
- Create: `build/build-installer.bat`
- Test: Generated installer on clean Windows VM

**Rationale:** Inno Setup creates professional Windows installers that can bundle the executable or install Python automatically.

- [ ] **Step 1: Create Inno Setup script**

```iss
; build/create-installer.iss
; Inno Setup script for Windows Automation Toolkit

#define MyAppName "Windows Automation Toolkit"
#define MyAppVersion "2.0.1"
#define MyAppPublisher "Your Name"
#define MyAppExeName "WindowsAutomationToolkit.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
OutputDir=..\installer
OutputBaseFilename=WindowsAutomationToolkit-Setup
SetupIconFile=..\assets\toolkit.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64
MinVersion=10.0.14393

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "{cm:AutoStartProgram,{#MyAppName}}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\launcher\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; Include any additional files needed

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autostartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startupicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Check if running on Windows 10 or later
  if (GetWindowsVersion < $0A000000) then
  begin
    MsgBox('This application requires Windows 10 or later.', mbError, MB_OK);
    Result := False;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Add any post-installation tasks here
  end;
end;
```

- [ ] **Step 2: Create installer build batch file**

```batch
:: build/build-installer.bat
@echo off
echo Building Windows Automation Toolkit Installer...

:: Check if Inno Setup is installed
set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" (
    echo Inno Setup not found. Please install from: https://jrsoftware.org/isdl.php
    exit /b 1
)

:: Build the installer
"%ISCC%" "create-installer.iss"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Installer built successfully!
    echo   Location: installer\WindowsAutomationToolkit-Setup.exe
) else (
    echo.
    echo ✗ Build failed!
)

pause
```

- [ ] **Step 3: Test installer on clean Windows VM**

```powershell
# Run the installer silently
.\installer\WindowsAutomationToolkit-Setup.exe /VERYSILENT

# Run the installed application
"C:\Program Files\Windows Automation Toolkit\WindowsAutomationToolkit.exe"
```

Expected: Installs and runs toolkit without Python

- [ ] **Step 4: Commit**

```bash
git add build/create-installer.iss build/build-installer.bat
git commit -m "feat: add Inno Setup installer for professional Windows installation"
```

---

### Task 4: Documentation Update

**Files:**
- Create: `docs/INSTALLATION.md`
- Modify: `Readme.md`

**Rationale:** Users need clear guidance on which installation method to choose.

- [ ] **Step 1: Create comprehensive installation guide**

```markdown
# Installation Guide - Windows Automation Toolkit

## Choose Your Installation Method

### Method 1: PowerShell One-Liner (Recommended for Quick Use)

**No Python required** - Automatically installs Python if needed.

```powershell
powershell -ExecutionPolicy Bypass "iwr https://raw.githubusercontent.com/yourusername/windows-automation-toolkit/main/scripts/install-toolkit.ps1 | iex"
```

**Pros:**
- ✅ Single command
- ✅ Auto-installs dependencies
- ✅ Always gets latest version

**Cons:**
- ❌ Requires internet connection
- ❌ Slower initial startup

---

### Method 2: Standalone Executable (Recommended for Offline Use)

**No Python required** - Bundled Python runtime.

1. Download from [Releases](https://github.com/yourusername/windows-automation-toolkit/releases)
2. Run `WindowsAutomationToolkit.exe`

**Pros:**
- ✅ No installation needed
- ✅ Works offline
- ✅ Fast startup

**Cons:**
- ❌ Larger download (~50 MB)
- ❌ Manual updates

---

### Method 3: Traditional Installer (Recommended for IT Deployment)

**No Python required** - Professional Windows installer.

1. Download `WindowsAutomationToolkit-Setup.exe` from Releases
2. Run installer
3. Launch from Start Menu or Desktop

**Pros:**
- ✅ Professional installation
- ✅ Start Menu integration
- ✅ Easy uninstall via Control Panel
- ✅ Good for enterprise deployment

**Cons:**
- ❌ Requires download
- ❌ Installation step needed

---

### Method 4: Python Source (For Developers)

**Requires Python 3.10+**

```bash
git clone https://github.com/yourusername/windows-automation-toolkit
cd windows-automation-toolkit
pip install -r requirements.txt
python main.py
```

**Pros:**
- ✅ Full source code access
- ✅ Easy to modify
- ✅ Smallest download

**Cons:**
- ❌ Requires Python installation
- ❌ Manual dependency management

---

## System Requirements

- **OS:** Windows 10 version 1903 or later (64-bit)
- **RAM:** 512 MB minimum
- **Disk:** 100 MB free space
- **Privileges:** Administrator rights for full functionality

## Troubleshooting

### PowerShell scripts won't run
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Executable blocked by SmartScreen
Right-click → Properties → Check "Unblock" → OK

### Python installation fails
Manually install Python from https://python.org, then use Method 4

### Winget not found
Install from Microsoft Store: https://aka.ms/winget
```

- [ ] **Step 2: Update main README**

Add to `Readme.md` after Features section:

```markdown
## Installation Options

Choose the method that works best for you:

### Quick Install (No Python Required)
```powershell
powershell -ExecutionPolicy Bypass "iwr https://raw.githubusercontent.com/yourusername/windows-automation-toolkit/main/scripts/install-toolkit.ps1 | iex"
```

### Download Executable
Get the standalone `.exe` from [Releases](https://github.com/yourusername/windows-automation-toolkit/releases) - no Python needed!

### Full Installation Guide
See [docs/INSTALLATION.md](docs/INSTALLATION.md) for all available methods.
```

- [ ] **Step 3: Commit**

```bash
git add docs/INSTALLATION.md Readme.md
git commit -m "docs: add comprehensive installation guide with Python alternatives"
```

---

### Task 5: GitHub Releases Configuration

**Files:**
- Create: `.github/workflows/release.yml`
- Create: `.github/workflows/build-executable.yml`

**Rationale:** Automate building and publishing executables/installers.

- [ ] **Step 1: Create GitHub Actions workflow for releases**

```yaml
# .github/workflows/release.yml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-executable:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Build executable
      run: |
        python build/build-executable.py
    
    - name: Upload executable artifact
      uses: actions/upload-artifact@v4
      with:
        name: toolkit-executable
        path: launcher/WindowsAutomationToolkit.exe
    
  build-installer:
    needs: build-executable
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Download executable
      uses: actions/download-artifact@v4
      with:
        name: toolkit-executable
        path: launcher/
    
    - name: Build installer
      run: |
        .\build\build-installer.bat
    
    - name: Upload installer artifact
      uses: actions/upload-artifact@v4
      with:
        name: toolkit-installer
        path: installer/WindowsAutomationToolkit-Setup.exe
    
  create-release:
    needs: [build-executable, build-installer]
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Download all artifacts
      uses: actions/download-artifact@v4
    
    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: |
          toolkit-executable/WindowsAutomationToolkit.exe
          toolkit-installer/WindowsAutomationToolkit-Setup.exe
        body: |
          ## Changes
          - Standalone executable (no Python required)
          - Windows installer package
          - PowerShell launcher script
          
          ## Installation
          See [INSTALLATION.md](docs/INSTALLATION.md) for details.
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 2: Create workflow for PR builds**

```yaml
# .github/workflows/build-executable.yml
name: Build Executable

on:
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Build executable
      run: |
        python build/build-executable.py
    
    - name: Test executable exists
      run: |
        if (Test-Path "launcher\WindowsAutomationToolkit.exe") {
          Write-Host "✓ Executable built successfully"
        } else {
          Write-Host "✗ Executable not found"
          exit 1
        }
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/release.yml .github/workflows/build-executable.yml
git commit -m "ci: add GitHub Actions workflows for automated releases"
```

---

## Testing Checklist

- [ ] Test PowerShell script on Windows 10 VM without Python
- [ ] Test standalone executable on Windows 10 VM without Python
- [ ] Test Inno Setup installer on Windows 10 VM without Python
- [ ] Verify all methods work with admin privileges
- [ ] Verify all methods work without admin privileges (limited functionality)
- [ ] Test SmartScreen compatibility
- [ ] Test Windows Defender compatibility
- [ ] Verify file sizes are reasonable (<100 MB)

---

## Success Criteria

1. ✅ User can run toolkit with single PowerShell command (no Python pre-installed)
2. ✅ User can download and run .exe directly (no Python pre-installed)
3. ✅ User can install via professional installer (no Python pre-installed)
4. ✅ All methods work on clean Windows 10/11 installation
5. ✅ Documentation clearly explains all installation options
6. ✅ Automated builds produce working executables

---

## Future Enhancements (Out of Scope)

- MSIX package for Microsoft Store distribution
- ClickOnce deployment
- Chocolatey package
- winget package
- Portable mode (USB drive)
- Auto-update mechanism
