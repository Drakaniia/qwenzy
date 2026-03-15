# Installation Guide - Windows Automation Toolkit

## Choose Your Installation Method

### Method 1: PowerShell One-Liner (Recommended for Quick Use)

**No Python required** - Automatically installs Python if needed.

```powershell
powershell -ExecutionPolicy Bypass "iwr -UseBasicParsing https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install-toolkit.ps1 | iex"
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

1. Download from [Releases](https://github.com/Drakaniia/qwenzy/releases)
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
git clone https://github.com/Drakaniia/qwenzy
cd qwenzy
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
