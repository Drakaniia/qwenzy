# Deployment Checklist - Windows Automation Toolkit

This guide helps you configure and deploy the Windows Automation Toolkit for distribution.

## Pre-Deployment Configuration

> **Note:** This repository is already configured with `Drakaniia/qwenzy`. Only update if you're forking.

### 1. Update GitHub Repository URLs (If Forking)

**Files to modify:**

#### `scripts/run-toolkit.ps1` (Line 11)
```powershell
# Current (Drakaniia/qwenzy):
$ToolkitRepo = "https://github.com/Drakaniia/qwenzy"

# Change to your fork:
$ToolkitRepo = "https://github.com/YOUR_USERNAME/qwenzy"
```

#### `scripts/install-toolkit.ps1` (Line 6)
```powershell
# Current (Drakaniia/qwenzy):
$ScriptUrl = "https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/run-toolkit.ps1"

# Change to your fork:
$ScriptUrl = "https://raw.githubusercontent.com/YOUR_USERNAME/qwenzy/main/scripts/run-toolkit.ps1"
```

#### `docs/INSTALLATION.md` (Multiple locations)
Replace all instances of `Drakaniia/qwenzy` with your fork's path.

#### `Readme.md` (Multiple locations)
Replace all instances of `Drakaniia/qwenzy` with your fork's path.

---

### 2. Generate Unique AppId GUID (Inno Setup)

The Inno Setup installer requires a unique application ID.

**Generate a new GUID:**
```powershell
# Run in PowerShell
[Guid]::NewGuid().ToString()
```

**Update `build/create-installer.iss` (Line 9):**
```iss
; Change from:
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}

; To (use your generated GUID):
AppId={{12345678-ABCD-EF12-3456-7890ABCDEF12}
```

---

### 3. Update Publisher Information

**Update `build/create-installer.iss` (Line 5):**
```iss
; Change from:
#define MyAppPublisher "Your Name"

; To:
#define MyAppPublisher "Your Name or Organization"
```

---

### 4. Application Icon (Optional)

If you want a custom icon for the executable and installer:

1. Create a 256x256 pixel ICO file
2. Save it as `assets/toolkit.ico`
3. The build scripts will automatically include it

**If you don't have an icon**, remove these lines:

**`build/toolkit.spec` (Line 58):**
```python
# Remove or comment out:
icon='../assets/toolkit.ico',
```

**`build/create-installer.iss` (Line 19):**
```iss
; Remove or comment out:
SetupIconFile=..\assets\toolkit.ico
```

---

## Build and Test Locally

Before deploying to GitHub, test everything locally:

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Build Executable
```bash
python build/build-executable.py
```

**Expected output:**
```
✓ Executable built successfully!
  Location: launcher/WindowsAutomationToolkit.exe
  Size: ~50 MB
```

### Step 3: Build Installer (Requires Inno Setup)

**Install Inno Setup:** https://jrsoftware.org/isdl.php

```bash
cd build
.\build-installer.bat
```

**Expected output:**
```
✓ Installer built successfully!
  Location: installer\WindowsAutomationToolkit-Setup.exe
```

### Step 4: Test on Clean Windows VM

Test all three installation methods on a clean Windows 10/11 VM:

1. **PowerShell One-Liner:**
   ```powershell
   powershell -ExecutionPolicy Bypass "iwr https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install-toolkit.ps1 | iex"
   ```

2. **Standalone Executable:**
   - Copy `launcher/WindowsAutomationToolkit.exe` to VM
   - Run and verify it works

3. **Installer:**
   - Copy `installer/WindowsAutomationToolkit-Setup.exe` to VM
   - Run installer and verify installation

---

## Deploy to GitHub

### Step 1: Initialize Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: Windows Automation Toolkit with Python alternatives"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository named `qwenzy`
3. Follow the instructions to push your code

### Step 3: Push Your Code
```bash
git remote add origin https://github.com/Drakaniia/qwenzy.git
git branch -M main
git push -u origin main
```

### Step 4: Create a Release Tag
```bash
# Tag your current commit
git tag -a v2.0.1 -m "Release v2.0.1 - Python alternatives included"

# Push the tag (triggers GitHub Actions release workflow)
git push origin v2.0.1
```

---

## GitHub Actions Setup

### Enable Workflows

After pushing to GitHub:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Enable workflows if prompted
4. The workflows will run automatically:
   - `build-executable.yml` - Runs on pull requests
   - `release.yml` - Runs on version tags (v*)

### Verify Release

After pushing a version tag:

1. Go to **Actions** tab
2. Wait for all jobs to complete (green checkmarks)
3. Go to **Releases** on the right sidebar
4. Verify the release includes:
   - `WindowsAutomationToolkit.exe` (~50 MB)
   - `WindowsAutomationToolkit-Setup.exe` (~55 MB)

---

## Post-Deployment Verification

### Test Installation Methods

1. **PowerShell One-Liner** (on clean Windows VM):
   ```powershell
   powershell -ExecutionPolicy Bypass "iwr https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install-toolkit.ps1 | iex"
   ```

2. **Download from Releases:**
   - Go to https://github.com/Drakaniia/qwenzy/releases
   - Download the executable or installer
   - Test on clean Windows VM

### Verify Documentation

Ensure all links in documentation point to your repository:
- [ ] `Readme.md` installation links
- [ ] `docs/INSTALLATION.md` download links
- [ ] All `yourusername` placeholders replaced

---

## Troubleshooting

### GitHub Actions Build Fails

**Common issues:**

1. **PyInstaller build fails:**
   ```
   Error: ModuleNotFoundError: No module named 'src.modules.xxx'
   ```
   **Fix:** Ensure all modules are listed in `hiddenimports` in `toolkit.spec`

2. **Inno Setup build fails:**
   ```
   Error: Source file "..\launcher\WindowsAutomationToolkit.exe" not found
   ```
   **Fix:** Ensure executable is built first (check workflow dependencies)

3. **Release creation fails:**
   ```
   Error: Not found
   ```
   **Fix:** Ensure `GITHUB_TOKEN` permissions allow release creation

### SmartScreen Warnings

Users may see SmartScreen warnings for unsigned executables:

**Solutions:**
1. **Short-term:** Document how to bypass SmartScreen
2. **Long-term:** Purchase code signing certificate from trusted CA

### PowerShell Execution Policy

Users may encounter execution policy errors:

**Solution:** Document in README:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Distribution Channels (Optional)

After successful GitHub deployment, consider:

### 1. winget Package
```bash
# Submit to Windows Package Manager Community Manifest
# https://github.com/microsoft/winget-pkgs
```

### 2. Chocolatey Package
```bash
# Create and submit Chocolatey package
# https://chocolatey.org/docs
```

### 3. Microsoft Store (MSIX)
```bash
# Use MSIX Packaging Tool to create Store package
# https://learn.microsoft.com/en-us/windows/msix/overview
```

---

## Security Best Practices

### Code Signing
- Sign PowerShell scripts with trusted certificate
- Sign executables to avoid SmartScreen warnings

### Hash Verification
- Publish SHA256 hashes of releases
- Add hash verification to PowerShell scripts

### Regular Updates
- Keep dependencies updated
- Monitor security advisories for PyInstaller, Inno Setup

---

## Checklist Summary

- [ ] Replace `yourusername` in all files (4 files)
- [ ] Generate unique AppId GUID for Inno Setup
- [ ] Update publisher name in ISS file
- [ ] Create or remove icon references
- [ ] Test executable build locally
- [ ] Test installer build locally (if Inno Setup available)
- [ ] Test on clean Windows VM
- [ ] Push to GitHub
- [ ] Create version tag
- [ ] Verify GitHub Actions workflows
- [ ] Verify release assets
- [ ] Update documentation links
- [ ] Test installation from released assets

---

## Support

For issues or questions:
- Check existing issues: https://github.com/Drakaniia/qwenzy/issues
- Create new issue with detailed description
- Include Windows version and error messages
