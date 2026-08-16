# Release v2.2.0 - Modular Architecture & More Optimization Apps

## What's New
- **Modular TUI service layer**: split the monolithic service module into focused modules for data models, action catalog sections, PowerShell script generation, and action executors.
- **Modular utilities**: `SystemUtils` is now composed from dedicated console UI, PowerShell, package manager, and filesystem mixins with an unchanged public API.
- **AutoHotKey package**: the AutoHotKey manager is organized into installation, script, runtime, and startup modules.
- **New optimization apps**: install **BleachBit** and **MemReduct** from the Debloat tab via winget or Chocolatey, alongside Windows Memory Cleaner.
- **CLI entry point**: the toolkit is available as a `windows-toolkit` console command.
- Package version is now sourced from `src/__init__.py` (the separate `VERSION` file was removed).

## Housekeeping
- Renamed `Readme.md` to `README.md` and updated all references and tests.
- Added `.gitattributes` to normalize line endings (LF for source/docs, CRLF for Windows scripts).
- Removed the unused `requests` dependency and obsolete files (superseded workflow, archived plan doc, placeholder release executable).

## Installation

```powershell
powershell -ExecutionPolicy Bypass "iwr -UseBasicParsing https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install.ps1 | iex"
```

---

# Release v2.1.5 - Smaller Windows Toolkit Download

## What's New
- Reworked the local PowerShell build script to use an isolated build virtualenv.
- Reduced the release zip from about 64 MB to about 14 MB by avoiding unrelated global Python packages.
- The build script now creates both `WindowsToolkit.exe` and `WindowsToolkit.zip` in `launcher`.

## Bug Fixes
- Prevented polluted local Python environments from bloating PyInstaller release assets.
- Added `.build-venv/` to `.gitignore`.

## Installation

```powershell
powershell -ExecutionPolicy Bypass "iwr -UseBasicParsing https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install.ps1 | iex"
```

---

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
