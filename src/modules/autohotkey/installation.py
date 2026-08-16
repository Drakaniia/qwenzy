"""AutoHotKey installation and detection."""

import os
import subprocess


class AutoHotKeyInstallMixin:
    """AutoHotKey installation and detection helpers."""

    def check_autohotkey_installed(self):
        """Check if AutoHotKey is installed"""
        # Common AutoHotkey installation paths
        common_paths = [
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe",
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey32.exe",
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe",
            r"C:\Program Files\AutoHotkey\AutoHotkey64.exe",
            r"C:\Program Files\AutoHotkey\AutoHotkey32.exe",
            r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
            r"C:\Program Files (x86)\AutoHotkey\v2\AutoHotkey64.exe",
            r"C:\Program Files (x86)\AutoHotkey\v2\AutoHotkey32.exe",
            r"C:\Program Files (x86)\AutoHotkey\v2\AutoHotkey.exe",
            r"C:\Program Files (x86)\AutoHotkey\AutoHotkey64.exe",
            r"C:\Program Files (x86)\AutoHotkey\AutoHotkey32.exe",
            r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
        ]

        # Check if any of the common paths exist
        for path in common_paths:
            if os.path.exists(path):
                self.ahk_executable = path
                return True

        # Try checking with winget
        try:
            result = subprocess.run(
                ["winget", "list", "--id", "AutoHotkey.AutoHotkey"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and "AutoHotkey" in result.stdout:
                return True
        except:
            pass

        # Try to find it in PATH
        try:
            result = subprocess.run(
                ["where", "AutoHotkey64.exe"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                self.ahk_executable = result.stdout.strip().split('\n')[0]
                return True
        except:
            pass

        return False

    def install_autohotkey(self):
        """Install AutoHotKey using winget"""
        print("\nInstalling AutoHotKey...")
        print("=" * 40)

        if self.check_autohotkey_installed():
            print("AutoHotKey is already installed")
            self.system.pause_execution()
            return

        # Check if winget is available
        if not self.system.check_program_exists("winget"):
            print("Winget is not available. Please install Windows Package Manager first.")
            print("Alternatively, download AutoHotKey from: https://www.autohotkey.com/")
            self.system.pause_execution()
            return

        if not self.system.get_confirmation("Install AutoHotKey using winget?"):
            print("Installation cancelled")
            return

        try:
            command = [
                "winget", "install",
                "--id", "AutoHotkey.AutoHotkey",
                "--accept-package-agreements",
                "--accept-source-agreements",
                "--silent"
            ]

            print(f"Executing: {' '.join(command)}")

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print("AutoHotKey installed successfully")
            else:
                print(f"Failed to install AutoHotKey: {result.stderr}")

        except subprocess.TimeoutExpired:
            print("AutoHotKey installation timed out")
        except Exception as e:
            print(f"Error installing AutoHotKey: {e}")

        self.system.pause_execution()
