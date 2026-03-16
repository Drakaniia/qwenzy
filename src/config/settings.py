"""
Configuration settings for Windows Automation Toolkit
"""

# PowerShell Scripts Configuration
POWERSHELL_SCRIPTS = {
    "debloat": {
        "win11debloat": {
            "name": "Win11Debloat",
            "url": "https://debloat.raphi.re/",
            "description": "Comprehensive Windows 11 debloating"
        },
        "debloat11": {
            "name": "Debloat11",
            "url": "https://git.io/debloat11",
            "description": "Alternative Windows 11 debloating"
        }
    },
    "tweaks": {
        "windows_tweaks": {
            "name": "Windows Tweaks",
            "url": "https://christitus.com/win",
            "description": "Windows performance and UI tweaks"
        }
    },
    "activation": {
        "activate_windows": {
            "name": "Windows Activation",
            "url": "https://get.activated.win",
            "description": "Windows activation script"
        }
    },
    "memory_cleaner": {
        "winmemorycleaner": {
            "name": "Windows Memory Cleaner",
            "description": "Open-source memory cleaner for Windows",
            "install_methods": {
                "choco": "choco install winmemorycleaner",
                "winget": "winget install IgorMundstein.WinMemoryCleaner"
            }
        }
    }
}

# Windows Run Commands
WINDOWS_COMMANDS = {
    "performance": "SystemPropertiesPerformance",
    "system": "sysdm.cpl",
    "power": "powercfg.cpl",
    "programs": "appwiz.cpl",
    "network": "ncpa.cpl"
}

# Essential Apps Configuration
ESSENTIAL_APPS = [
    {"id": "Microsoft.VisualStudioCode", "name": "Visual Studio Code", "versions": ["latest"], "download_url": "https://code.visualstudio.com/download"},
    {"id": "Yandex.Browser", "name": "Yandex Browser", "versions": ["latest"], "download_url": "https://browser.yandex.com/download/"},
    {"id": "OpenJS.NodeJS", "name": "Node.js LTS", "versions": ["latest", "18.x", "20.x"], "download_url": "https://nodejs.org/en/download"},
    {"id": "Python.Python.3", "name": "Python 3", "versions": ["latest", "3.11", "3.12"], "download_url": "https://www.python.org/downloads/"},
    {"id": "Git.Git", "name": "Git", "versions": ["latest"], "download_url": "https://git-scm.com/download/win"},
    {"id": "AutoHotkey.AutoHotkey", "name": "AutoHotKey", "versions": ["latest"], "download_url": "https://www.autohotkey.com/download/"}
]

# Terminal AI Tools Configuration
AI_TOOLS = [
    {"package": "opencode-ai", "name": "OpenCode AI"},
    {"package": "@qwen-code/qwen-code@latest", "name": "Qwen Code CLI"}
]

# Power Plan Configuration
ULTIMATE_PERFORMANCE_GUID = "e9a42b02-d5df-448d-aa00-03f14749eb61"

# AutoHotKey Script Content
AHK_SCRIPT_CONTENT = """; ===============================
; Full F3 -> Left Mouse Button
; ===============================

#Requires AutoHotkey v2.0

; --- Single Click / Hold / Drag ---
F3::
{
    SendInput("{LButton down}")   ; Press & hold left button
    KeyWait("F3")                 ; Wait until F3 is released
    SendInput("{LButton up}")     ; Release button
}

; AHK v2 version - Remap Middle Mouse Button to Back
MButton::Send("!{Left}")
"""

# PowerShell Script to configure 3-finger tap to go back
TOUCHPAD_THREE_FINGER_BACK_SCRIPT = """
# Configure 3-finger tap to go back (instead of opening task view)
Write-Host "Configuring touchpad 3-finger tap to go back..."
Write-Host ""

# Try to open Windows Settings to the Touchpad page
Write-Host "Opening Windows Settings to Touchpad configuration..."
Start-Process "ms-settings:devices-touchpad"

Write-Host ""
Write-Host "================================================================================"
Write-Host "MANUAL CONFIGURATION REQUIRED"
Write-Host "================================================================================"
Write-Host ""
Write-Host "Windows 10/11 touchpad settings cannot be fully automated via registry."
Write-Host "Please follow these steps to configure 3-finger tap:"
Write-Host ""
Write-Host "1. In the Settings window that opened, scroll down to 'Three-finger gestures'"
Write-Host "2. Look for the 'Taps' section"
Write-Host "3. Change it from 'Open task view' to 'Back'"
Write-Host ""
Write-Host "Alternative method:"
Write-Host "1. Press Windows key + I to open Settings"
Write-Host "2. Go to Bluetooth & devices > Touchpad"
Write-Host "3. Scroll down to 'Three-finger gestures'"
Write-Host "4. Set 'Taps' to 'Back'"
Write-Host ""
Write-Host "================================================================================"
Write-Host ""
Write-Host "Note: The AutoHotkey script (F3 and Middle Mouse) is separate from"
Write-Host "touchpad gestures and will continue to work independently."
"""

# UI Configuration
UI_CONFIG = {
    "header_title": "Windows Automation Toolkit",
    "header_subtitle": "Windows 10/11 Optimization Suite",
    "menu_options": {
        "1": {"title": "Windows Debloat & Tweaks"},
        "2": {"title": "Windows Settings & Run Commands"},
        "3": {"title": "Unlock Ultimate Performance"},
        "4": {"title": "Install Essential Apps"},
        "5": {"title": "Install Terminal AI Tools"},
        "6": {"title": "Setup AutoHotKey"},
        "0": {"title": "Exit"}
    }
}

# System Paths
SYSTEM_PATHS = {
    "documents": "Documents",
    "startup": "APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup",
    "temp": "TEMP"
}