# Release v2.1.4 - Textual Windows Toolkit Executable

## What's New
- Rebuilt the GitHub release executable from the current Textual TUI entry point.
- Fixed release automation to publish `WindowsToolkit.exe` and `WindowsToolkit.zip`.
- Bundled Textual lazy widget modules required by the packaged executable.

## Bug Fixes
- Fixed the latest-release download opening the old numbered-menu CLI build.
- Removed stale PyInstaller hidden imports for deleted modules.
- Prevented the old release-published workflow from uploading duplicate assets.

## Installation

```powershell
powershell -ExecutionPolicy Bypass "iwr -UseBasicParsing https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install.ps1 | iex"
```

---

# Release v2.1.2 - Windows Toolkit Executable

## What's New
- 🚀 **Standalone Executable**: Download and run without Python!
- 🔧 Fixed installation scripts to work with GitHub releases
- 📦 Added both .exe and .zip distribution formats

## Bug Fixes
- Fixed install.ps1 script to download from proper GitHub releases URL
- Resolved missing release assets issue

## Changes
- Created GitHub release v2.1.2-release with WindowsAutomationToolkit.exe and WindowsAutomationToolkit.zip
- Updated build process to generate proper release assets

## Installation

### Option 1: Download Executable (Recommended)
```powershell
powershell -ExecutionPolicy Bypass "iwr -UseBasicParsing https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/run-exe.ps1 | iex"
```

### Option 2: Manual Installation
```bash
git clone https://github.com/Drakaniia/qwenzy.git
cd qwenzy
pip install -r requirements.txt
python main.py
```

## Features
- Windows Debloat & Tweaks
- Automated Windows Optimization
- Power Management (Ultimate Performance plan)
- AutoHotKey Manager

## Notes
- Requires Windows 10/11
- Administrator privileges recommended
- The executable includes console support for user input

---

# Release v2.1.0 - Standalone Executable

## What's New
- 🚀 **Standalone Executable**: Download and run without Python!
- 🔧 Fixed PowerShell launcher to install dependencies automatically
- 📦 Added GitHub Actions workflow for auto-building releases

## Installation

### Option 1: Download Executable (Recommended)
```powershell
powershell -ExecutionPolicy Bypass "iwr -UseBasicParsing https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/run-exe.ps1 | iex"
```

### Option 2: Manual Installation
```bash
git clone https://github.com/Drakaniia/qwenzy.git
cd qwenzy
pip install -r requirements.txt
python main.py
```

## Features
- Windows Debloat & Tweaks
- Automated Windows Optimization
- Power Management (Ultimate Performance plan)
- AutoHotKey Manager

## Notes
- Requires Windows 10/11
- Administrator privileges recommended
- The executable includes console support for user input
