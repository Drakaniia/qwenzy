"""AutoHotKey script runtime control."""

import subprocess


class AutoHotKeyRuntimeMixin:
    """AutoHotKey script run, stop, and status checks."""

    def run_script(self):
        """Run the AutoHotKey script"""
        print("\n▶️ Running AutoHotKey Script...")
        print("=" * 40)

        if not self.check_autohotkey_installed():
            print("AutoHotKey is not installed. Please install it first.")
            self.system.pause_execution()
            return

        script_path = self.get_script_path()
        if not script_path:
            print(" AutoHotKey script not found. Please create it first.")
            self.system.pause_execution()
            return

        if self.is_script_running():
            print("ℹ️ Script is already running")
            self.system.pause_execution()
            return

        try:
            print(f"Starting script: {script_path}")

            # Start AutoHotKey script
            subprocess.Popen([self.ahk_executable, script_path])

            # Give it a moment to start
            import time
            time.sleep(2)

            if self.is_script_running():
                print("AutoHotKey script is now running")
                print("\nActive Features:")
                print("• F3 → Left Mouse Button (hold/drag)")
                print("• Middle Mouse → Browser Back")
            else:
                print("Failed to start script")

        except Exception as e:
            print(f"Error running script: {e}")

        self.system.pause_execution()

    def stop_script(self):
        """Stop the AutoHotKey script"""
        print("\n⏹️ Stopping AutoHotKey Script...")
        print("=" * 40)

        if not self.is_script_running():
            print("ℹ️ No AutoHotKey script is currently running")
            self.system.pause_execution()
            return

        try:
            # Find and kill AutoHotKey processes
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq AutoHotkey64.exe"],
                capture_output=True,
                text=True
            )

            if "AutoHotkey64.exe" in result.stdout:
                # Kill all AutoHotKey processes
                subprocess.run(["taskkill", "/F", "/IM", "AutoHotkey64.exe"],
                             capture_output=True)
                print(" AutoHotKey script stopped")
            else:
                print("ℹ️ No AutoHotKey processes found")

        except Exception as e:
            print(f" Error stopping script: {e}")

        self.system.pause_execution()

    def is_script_running(self):
        """Check if the AutoHotKey script is currently running"""
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq AutoHotkey64.exe"],
                capture_output=True,
                text=True
            )
            return "AutoHotkey64.exe" in result.stdout
        except:
            return False
