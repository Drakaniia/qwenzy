# Windows Automation Toolkit v2.0.1

A comprehensive Windows 10/11 optimization and productivity toolkit that automates system tweaks, software installation, and configuration tasks.

## Features

- **Windows Debloat & Tweaks** - Remove bloatware, optimize system settings
- **Power Management** - Unlock Ultimate Performance plan, manage power profiles
- **App Installer** - Install apps via Winget
- **AI Tools Installer** - Quick setup for AI development tools
- **AutoHotKey Manager** - Manage automation scripts

## Installation Options

Choose the method that works best for you:

### Option 1: Download Executable (Fastest, Recommended)
**Best for:** Quick use, no Python installation needed

```powershell
powershell -ExecutionPolicy Bypass "iwr -UseBasicParsing https://github.com/Drakaniia/qwenzy/releases/latest/download/WindowsToolkit.zip -OutFile $env:TEMP\toolkit.zip; Expand-Archive $env:TEMP\toolkit.zip $env:TEMP -Force; & $env:TEMP\WindowsToolkit.exe"
```

This will:
- Download the latest `.zip` from Releases
- Extract and launch the toolkit immediately
- No Python required

Or download manually from [Releases](https://github.com/Drakaniia/qwenzy/releases)

### Option 2: Manual Installation
**Best for:** Developers, contributors

```bash
git clone https://github.com/Drakaniia/qwenzy.git
cd qwenzy
pip install -r requirements.txt
python main.py
```

Or build your own executable:
```bash
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass ".\scripts\build-exe.ps1"
```

## Requirements

- Windows 10/11
- Administrator privileges (recommended)
- Internet connection (for downloads)
- Windows Package Manager (winget) - for app installation features

## Usage

1. Launch the toolkit (via executable or `python main.py`)
2. Accept admin privileges when prompted
3. Navigate the menu to access different modules
4. All operations require confirmation before execution

## Troubleshooting

- **Winget not found**: Install Windows Package Manager from Microsoft Store
- **PowerShell scripts blocked**: Run as administrator
- **Node.js required**: Install via Essential Apps installer before using AI tools

## License

Educational and personal use. Use at your own risk.
