"""AutoHotKey script file creation and management."""

import os


class AutoHotKeyScriptsMixin:
    """AutoHotKey script file creation, editing, and listing."""

    def create_script(self):
        """Create or update the AutoHotKey script"""
        print("\nCreating AutoHotKey Script...")
        print("=" * 40)

        # Create AutoHotKey directory
        ahk_dir = os.path.join(self.system.documents_folder, "AutoHotKey")

        if not self.system.ensure_directory_exists(ahk_dir):
            print("Failed to create AutoHotKey directory")
            self.system.pause_execution()
            return

        script_path = os.path.join(ahk_dir, self.ahk_script_name)

        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(self.script_content)

            print(f"AutoHotKey script created at: {script_path}")
            print("\nScript Content:")
            print("-" * 40)
            print(self.script_content)
            print("-" * 40)

        except Exception as e:
            print(f"Error creating AutoHotKey script: {e}")

        self.system.pause_execution()

    def get_script_path(self):
        """Get the path to the AutoHotKey script"""
        ahk_dir = os.path.join(self.system.documents_folder, "AutoHotKey")
        return os.path.join(ahk_dir, self.ahk_script_name)

    def edit_script(self):
        """Open the AutoHotKey script in default editor"""
        script_path = self.get_script_path()
        if not script_path or not os.path.exists(script_path):
            print("Script not found. Please create it first.")
            self.system.pause_execution()
            return

        try:
            os.startfile(script_path)
            print("Script opened in default editor")
        except Exception as e:
            print(f"Error opening script: {e}")

        self.system.pause_execution()

    def create_custom_script(self, script_name, script_content):
        """Create a custom AutoHotKey script"""
        ahk_dir = os.path.join(self.system.documents_folder, "AutoHotKey")

        if not self.system.ensure_directory_exists(ahk_dir):
            return False

        script_path = os.path.join(ahk_dir, f"{script_name}.ahk")

        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            print(f"Custom script created: {script_path}")
            return True
        except Exception as e:
            print(f"Error creating custom script: {e}")
            return False

    def list_scripts(self):
        """List all AutoHotKey scripts in the directory"""
        ahk_dir = os.path.join(self.system.documents_folder, "AutoHotKey")

        if not os.path.exists(ahk_dir):
            print("AutoHotKey directory not found")
            return []

        scripts = []
        try:
            for file in os.listdir(ahk_dir):
                if file.endswith('.ahk'):
                    scripts.append(file)
        except Exception as e:
            print(f"Error listing scripts: {e}")

    def list_ahk_scripts(self):
        """List all .ahk scripts in the AutoHotKey directory"""
        ahk_dir = self.get_ahk_directory()
        if not ahk_dir or not os.path.exists(ahk_dir):
            return []

        scripts = []
        try:
            for file in os.listdir(ahk_dir):
                if file.endswith('.ahk'):
                    scripts.append(file)
        except Exception as e:
            print(f"Error listing scripts: {e}")

        return scripts
