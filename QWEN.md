# Windows Automation Toolkit - Project Context

## Project Overview

**Windows Automation Toolkit** is a comprehensive Windows 10/11 optimization and productivity toolkit. It automates system tweaks, software installation, and configuration tasks through a menu-driven CLI interface.

**Current Version:** 2.0.1

**Core Features:**
- **Windows Debloat & Tweaks** - Remove bloatware via PowerShell scripts (Win11Debloat, Debloat11), optimize system settings
- **Power Management** - Unlock Ultimate Performance power plan, manage power profiles
- **App Installer** - Install essential apps via Windows Package Manager (winget)
- **AI Tools Installer** - Quick setup for AI development tools (OpenCode AI, Qwen Code CLI)
- **AutoHotKey Manager** - Manage automation scripts and configure remappings

## Project Structure

```
qwenzy/
├── main.py                 # Main entry point
├── setup.py                # Package setup configuration
├── requirements.txt        # Python dependencies
├── scripts/                # PowerShell build & install scripts
│   ├── build-exe.ps1       # PyInstaller build script
│   ├── install.ps1         # User installation script
│   └── run-exe.ps1         # Executable launcher
├── src/
│   ├── config/
│   │   └── settings.py     # Configuration constants (scripts, apps, UI)
│   ├── modules/
│   │   ├── debloat.py      # Windows debloating module
│   │   ├── settings.py     # Windows settings module
│   │   ├── power.py        # Power management module
│   │   ├── installer.py    # App installer module
│   │   ├── ai_tools.py     # AI tools installer module
│   │   └── autohotkey.py   # AutoHotKey manager module
│   └── utils/
│       └── system.py       # Core system utilities (admin check, PS execution)
├── tests/                  # Test files
└── docs/                   # Documentation
```

## Building and Running

### Prerequisites
- Windows 10/11
- Python 3.10+
- Administrator privileges (recommended for full functionality)
- Windows Package Manager (winget) - for app installation features

### Installation (Development)

```bash
# Clone and install dependencies
git clone https://github.com/Drakaniia/qwenzy.git
cd qwenzy
pip install -r requirements.txt

# Run the toolkit
python main.py
```

### Build Executable

```bash
# Install dependencies
pip install -r requirements.txt

# Build standalone executable
powershell -ExecutionPolicy Bypass ".\scripts\build-exe.ps1"

# Output: dist\WindowsToolkit.exe
```

### Run Executable

```powershell
# Via installer script (downloads latest release)
powershell -ExecutionPolicy Bypass "iwr https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install.ps1 | iex"

# Or run built executable directly
.\dist\WindowsToolkit.exe
```

### Run Tests

```bash
# Run pytest
pytest tests/
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.25.0 | HTTP requests for downloading scripts |
| `pyinstaller` | >=6.0.0 | Build standalone executables |

## Architecture

**Modular Design:** The toolkit uses a modular architecture with separate modules for each feature area:

1. **Main Entry Point** (`main.py`): `WindowsAutomationToolkit` class orchestrates all modules
2. **System Utilities** (`src/utils/system.py`): `SystemUtils` class provides core functionality:
   - Admin privilege detection and elevation
   - PowerShell command execution
   - User input/confirmation handling
   - System path resolution
3. **Configuration** (`src/config/settings.py`): Centralized configuration for:
   - PowerShell script URLs (Win11Debloat, Christitus Tweaks, etc.)
   - Essential apps list (VS Code, Node.js, Python, Git, AutoHotKey)
   - AI tools packages
   - UI menu configuration
4. **Feature Modules** (`src/modules/`): Each module handles a specific domain

## Development Conventions

**Coding Style:**
- Python 3.10+ syntax
- Class-based module design
- Type hints where applicable
- Docstrings for classes and public methods

**Testing:**
- Tests located in `tests/` directory
- Uses pytest framework
- Test files follow `test_*.py` naming convention

**Configuration:**
- All configurable values centralized in `src/config/settings.py`
- UI text and menu options defined in `UI_CONFIG` dictionary
- External script URLs stored in `POWERSHELL_SCRIPTS` dictionary

**Build Process:**
- PyInstaller for executable creation
- Single-file executable with embedded `src` directory
- Console mode (not windowed) for user input support

## Key Configuration Points

### PowerShell Scripts (External)
- Win11Debloat: `https://debloat.raphi.re/`
- Windows Tweaks: `https://christitus.com/win`
- Windows Activation: `https://get.activated.win`

### Essential Apps (Winget IDs)
- Visual Studio Code: `Microsoft.VisualStudioCode`
- Node.js LTS: `OpenJS.NodeJS`
- Python 3: `Python.Python.3`
- Git: `Git.Git`
- AutoHotKey: `AutoHotkey.AutoHotkey`

### AI Tools
- `opencode-ai`
- `@qwen-code/qwen-code@latest`

## Important Notes

- **Admin Privileges:** Toolkit requests admin elevation on launch for full functionality
- **User Confirmation:** All operations require user confirmation before execution
- **Interactive PowerShell:** Some scripts launch interactive PowerShell windows
- **Touchpad Configuration:** 3-finger gesture settings require manual Windows Settings configuration
