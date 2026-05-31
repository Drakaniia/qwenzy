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
