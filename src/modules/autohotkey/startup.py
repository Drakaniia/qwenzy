"""AutoHotKey Windows startup integration."""

import os
import shutil


class AutoHotKeyStartupMixin:
    """AutoHotKey script startup-folder integration."""

    def add_to_startup(self):
        """Add AutoHotKey script to Windows startup"""
        print("\nAdding Script to Startup...")
        print("=" * 40)

        script_path = self.get_script_path()
        if not script_path:
            print(" AutoHotKey script not found. Please create it first.")
            self.system.pause_execution()
            return

        startup_folder = self.system.get_system_path("startup")
        if not startup_folder:
            print(" Could not find startup folder")
            self.system.pause_execution()
            return

        shortcut_path = os.path.join(startup_folder, self.ahk_script_name)

        try:
            # Copy script to startup folder
            shutil.copy2(script_path, shortcut_path)
            print(f"Script added to startup: {shortcut_path}")
            print(" The script will automatically start when Windows boots")

        except Exception as e:
            print(f" Error adding script to startup: {e}")

        self.system.pause_execution()

    def remove_from_startup(self):
        """Remove AutoHotKey script from Windows startup"""
        print("\n🗑️ Removing Script from Startup...")
        print("=" * 40)

        startup_folder = self.system.get_system_path("startup")
        if not startup_folder:
            print(" Could not find startup folder")
            self.system.pause_execution()
            return

        shortcut_path = os.path.join(startup_folder, self.ahk_script_name)

        try:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                print(f" Script removed from startup: {shortcut_path}")
            else:
                print("ℹ️ Script not found in startup folder")

        except Exception as e:
            print(f" Error removing script from startup: {e}")

        self.system.pause_execution()

    def auto_start_all_on_boot(self):
        """Configure AutoHotKey script to run automatically on system startup"""
        print("\n Auto-Start All on Boot")
        print("=" * 40)

        # First, ensure AutoHotKey is installed
        if not self.check_autohotkey_installed():
            print("AutoHotKey is not installed")
            print("Installing AutoHotKey...")
            self.install_autohotkey()

            if not self.check_autohotkey_installed():
                print("Failed to install AutoHotKey. Cannot proceed with auto-start setup.")
                self.system.pause_execution()
                return

        # Ensure script is created
        script_path = self.get_script_path()
        if not script_path or not os.path.exists(script_path):
            print("Script does not exist, creating AutoHotKey script...")
            self.create_script()
            script_path = self.get_script_path()

            if not script_path or not os.path.exists(script_path):
                print("Failed to create AutoHotKey script.")
                self.system.pause_execution()
                return

        # Add to startup using the existing method
        print("Adding script to Windows startup...")
        startup_folder = self.system.get_system_path("startup")
        if not startup_folder:
            print("Could not find startup folder")
            self.system.pause_execution()
            return

        shortcut_path = os.path.join(startup_folder, self.ahk_script_name)

        try:
            # Copy the actual script to the startup folder
            shutil.copy2(script_path, shortcut_path)
            print(f"Script added to startup: {shortcut_path}")
            print(" The script will now run automatically every time Windows starts")
        except Exception as e:
            print(f"Error adding script to startup: {e}")
            self.system.pause_execution()
            return

        # Run the script now if not already running
        if not self.is_script_running():
            print("▶️ Starting script now...")
            self.run_script()

        print(" Auto-start setup completed successfully!")
        print(" The AutoHotKey script will now run automatically on every system startup")
        self.system.pause_execution()
        return
