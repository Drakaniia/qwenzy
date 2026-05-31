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
    "network": "ncpa.cpl"
}

# Automated Windows Optimization Actions
WINDOWS_OPTIMIZATION_ACTIONS = [
    {
        "id": "full",
        "title": "Run Full Windows Optimization",
        "target": "Windows 10/11 automated optimization",
        "description": "Apply the complete automated optimization set from OPTIMIZE.md.",
        "groups": ["restore_point", "cleanup", "network", "performance", "privacy", "interface", "services"],
        "risk": "High"
    },
    {
        "id": "cleanup",
        "title": "Clean Temporary and Update Caches",
        "target": "Temp, Prefetch, Windows Update, Store, NVIDIA caches",
        "description": "Remove disposable cache files that OPTIMIZE.md previously required cleaning manually.",
        "groups": ["restore_point", "cleanup"],
        "risk": "Medium"
    },
    {
        "id": "network",
        "title": "Apply Network Throughput Tweaks",
        "target": "TCP autotuning, CTCP, QoS, network adapter power saving",
        "description": "Apply the documented TCP/IP, QoS, and adapter energy-saving adjustments.",
        "groups": ["restore_point", "network"],
        "risk": "Medium"
    },
    {
        "id": "performance",
        "title": "Apply System Performance Tweaks",
        "target": "Power, Game Mode, Storage Sense, remote access, mouse and keyboard",
        "description": "Apply automated performance, power, gaming, peripheral, and background-activity settings.",
        "groups": ["restore_point", "performance"],
        "risk": "High"
    },
    {
        "id": "privacy",
        "title": "Apply Privacy and Telemetry Tweaks",
        "target": "Telemetry, advertising ID, activity history, location, app permissions",
        "description": "Disable privacy-sensitive Windows features and app permissions covered in OPTIMIZE.md.",
        "groups": ["restore_point", "privacy"],
        "risk": "High"
    },
    {
        "id": "interface",
        "title": "Apply Explorer and Interface Tweaks",
        "target": "Explorer, Start, taskbar, tips, suggestions, accessibility launchers",
        "description": "Apply File Explorer, Start menu, taskbar, notification suggestion, and accessibility tweaks.",
        "groups": ["restore_point", "interface"],
        "risk": "Medium"
    },
    {
        "id": "services",
        "title": "Disable Unnecessary Services",
        "target": "Telemetry, Xbox, Hyper-V, sensors, smart card, touch, indexing, SysMain",
        "description": "Disable optional background services listed in OPTIMIZE.md plus common extra optimization services.",
        "groups": ["restore_point", "services"],
        "risk": "High"
    }
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
        "4": {"title": "Automated Windows Optimization"},
        "5": {"title": "Setup AutoHotKey"},
        "0": {"title": "Exit"}
    }
}

# System Paths
SYSTEM_PATHS = {
    "documents": "Documents",
    "startup": "APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup",
    "temp": "TEMP"
}
