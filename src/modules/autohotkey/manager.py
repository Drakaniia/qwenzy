"""AutoHotKeyManager facade composing installation, script, runtime, and startup mixins."""

import os
import shutil
import subprocess

from src.config.settings import AHK_SCRIPT_CONTENT
from src.modules.autohotkey.installation import AutoHotKeyInstallMixin
from src.modules.autohotkey.runtime import AutoHotKeyRuntimeMixin
from src.modules.autohotkey.scripts import AutoHotKeyScriptsMixin
from src.modules.autohotkey.startup import AutoHotKeyStartupMixin


class AutoHotKeyManager(
    AutoHotKeyInstallMixin,
    AutoHotKeyScriptsMixin,
    AutoHotKeyRuntimeMixin,
    AutoHotKeyStartupMixin,
):
    """AutoHotKey setup and script management functionality"""

    def __init__(self, system_utils):
        self.system = system_utils
        self.script_content = AHK_SCRIPT_CONTENT
        self.ahk_executable = "AutoHotkey64.exe"
        self.ahk_script_name = "automation.ahk"

    def show_autohotkey_menu(self):
        """Display AutoHotKey menu"""
        while True:
            self.system.clear_screen()
            self.system.print_header("AutoHotKey Setup & Management")

            options = {
                "1": {"title": "Install AutoHotKey"},
                "2": {"title": "Create Script & Auto-Start on Boot"},
                "3": {"title": "Script Status"},
                "0": {"title": "Back to Main Menu"}
            }

            self.system.print_menu("AUTOHOTKEY OPTIONS", options)

            choice = self.system.get_menu_choice(options)

            if choice == "1":
                self.install_autohotkey()
            elif choice == "2":
                self.create_script_and_startup()
            elif choice == "3":
                self.show_script_status()
            elif choice == "0":
                return

    def create_script_and_startup(self):
        """Create script and add it to Windows startup"""
        print("\nCreating Script & Adding to Startup...")
        print("=" * 40)

        # First, ensure AutoHotKey is installed
        if not self.check_autohotkey_installed():
            print("AutoHotKey is not installed")
            print("Installing AutoHotKey...")
            self.install_autohotkey()

            if not self.check_autohotkey_installed():
                print("Failed to install AutoHotKey. Cannot proceed.")
                self.system.pause_execution()
                return

        # Stop any running AutoHotkey scripts
        if self.is_script_running():
            print("\n⏹️ Stopping running scripts...")
            try:
                subprocess.run(["taskkill", "/F", "/IM", "AutoHotkey64.exe"],
                             capture_output=True, timeout=10)
                print("✓ Stopped running scripts")
                import time
                time.sleep(1)
            except Exception as e:
                print(f"✗ Error stopping scripts: {e}")

        # Delete old script files
        ahk_dir = os.path.join(self.system.documents_folder, "AutoHotKey")
        script_path = os.path.join(ahk_dir, self.ahk_script_name)
        startup_folder = self.system.get_system_path("startup")
        startup_script_path = os.path.join(startup_folder, self.ahk_script_name) if startup_folder else None

        files_deleted = []
        for path in [script_path, startup_script_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                    files_deleted.append(path)
                    print(f"✓ Deleted old script: {path}")
                except Exception as e:
                    print(f"✗ Error deleting {path}: {e}")

        if not files_deleted:
            print("ℹ️ No old scripts found to delete")

        # Create the script
        if not self.system.ensure_directory_exists(ahk_dir):
            print("Failed to create AutoHotKey directory")
            self.system.pause_execution()
            return

        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(self.script_content)

            print(f"\n✓ Script created at: {script_path}")
            print("\nScript Content:")
            print("-" * 40)
            print(self.script_content)
            print("-" * 40)
        except Exception as e:
            print(f"✗ Error creating script: {e}")
            self.system.pause_execution()
            return

        # Add to startup
        if not startup_folder:
            print("✗ Could not find startup folder")
            self.system.pause_execution()
            return

        try:
            shutil.copy2(script_path, startup_script_path)
            print(f"\n✓ Script added to startup: {startup_script_path}")
            print("✓ The script will automatically start when Windows boots")
        except Exception as e:
            print(f"✗ Error adding script to startup: {e}")
            self.system.pause_execution()
            return

        # Start the script now
        print("\n▶️ Starting script now...")
        try:
            subprocess.Popen([self.ahk_executable, script_path])
            import time
            time.sleep(2)

            if self.is_script_running():
                print("✓ Script is now running")
                print("\nActive Features:")
                print("• F3 → Left Mouse Button (hold/drag)")
                print("• Middle Mouse → Browser Back")
            else:
                print("✗ Failed to start script")
        except Exception as e:
            print(f"✗ Error starting script: {e}")

        self.system.pause_execution()

    def show_script_status(self):
        """Show the current status of AutoHotKey and script"""
        print("\n AutoHotKey Status")
        print("=" * 40)

        # Check AutoHotKey installation
        ahk_installed = self.check_autohotkey_installed()
        print(f"AutoHotKey: {'Installed' if ahk_installed else 'Not Installed'}")

        if ahk_installed:
            # Check script existence
            script_path = self.get_script_path()
            script_exists = script_path and os.path.exists(script_path)
            print(f"Script: {'Created' if script_exists else 'Not Found'}")

            if script_exists:
                print(f" Location: {script_path}")

                # Check if script is running
                script_running = self.is_script_running()
                print(f"Status: {'Running' if script_running else 'Stopped'}")

                # Check startup status
                startup_folder = self.system.get_system_path("startup")
                if startup_folder:
                    shortcut_path = os.path.join(startup_folder, self.ahk_script_name)
                    in_startup = os.path.exists(shortcut_path)
                    print(f"Startup: {'Enabled' if in_startup else 'Disabled'}")

        self.system.pause_execution()
