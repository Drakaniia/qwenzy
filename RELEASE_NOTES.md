# Release v2.1.1 - Power Plan Fix & Visual Enhancements

## What's New
- 🔧 **Fixed Ultimate Performance Power Plan** - GUID extraction now works correctly for activation
- 🎨 **ASCII Title Display** - Visual title banner on startup
- 🚀 **Standalone Executable**: Download and run without Python!

## Bug Fixes
- Fixed regex pattern to extract GUIDs from `powercfg -duplicatescheme` output (with or without curly braces)
- Resolved issue where Ultimate Performance plan couldn't be activated after creation

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
- Power Management (Ultimate Performance plan)
- App Installer via Winget
- AI Tools Installer
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
- Power Management (Ultimate Performance plan)
- App Installer via Winget
- AI Tools Installer
- AutoHotKey Manager

## Notes
- Requires Windows 10/11
- Administrator privileges recommended
- The executable includes console support for user input
