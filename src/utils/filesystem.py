"""Filesystem and PATH lookup helpers."""

import os
import subprocess
from pathlib import Path


class FileSystemMixin:
    """Program detection, directory, and system path helpers."""

    def check_program_exists(self, program_name):
        """Check if a program is available in the system PATH"""
        # Try to refresh the PATH environment variable to catch recently installed programs
        os.environ.update(os.environ)

        # Special handling for Node.js and npm
        if program_name.lower() in ['node', 'nodejs']:
            node_variants = ['node', 'nodejs', 'node.exe', 'nodejs.exe']
            for variant in node_variants:
                try:
                    result = subprocess.run([variant, "--version"],
                                          capture_output=True, check=True, timeout=10)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    continue

            # Check common Node.js installation directories
            common_node_paths = [
                r"C:\Program Files\nodejs\node.exe",
                r"C:\Program Files (x86)\nodejs\node.exe",
                os.path.expanduser(r"~\AppData\Local\Programs\nodejs\node.exe")
            ]

            for path in common_node_paths:
                if os.path.exists(path):
                    try:
                        result = subprocess.run([path, "--version"],
                                              capture_output=True, check=True, timeout=10)
                        return True
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                        continue

            return False

        elif program_name.lower() == 'npm':
            npm_variants = ['npm', 'npm.cmd', 'npm.exe']
            for variant in npm_variants:
                try:
                    result = subprocess.run([variant, "--version"],
                                          capture_output=True, check=True, timeout=10)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    continue

            # Check npm in common Node.js installation directories
            common_npm_paths = [
                r"C:\Program Files\nodejs\npm.cmd",
                r"C:\Program Files (x86)\nodejs\npm.cmd",
                os.path.expanduser(r"~\AppData\Local\Programs\nodejs\npm.cmd")
            ]

            for path in common_npm_paths:
                if os.path.exists(path):
                    try:
                        result = subprocess.run([path, "--version"],
                                              capture_output=True, check=True, timeout=10)
                        return True
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                        continue

            return False
        else:
            # For other programs, use the original method
            try:
                subprocess.run([program_name, "--version"],
                             capture_output=True, check=True, timeout=10)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                return False

    def ensure_directory_exists(self, directory_path):
        """Ensure a directory exists, create if it doesn't"""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f" Failed to create directory {directory_path}: {e}")
            return False

    def get_system_path(self, path_key):
        """Get system path by key"""
        paths = {
            "documents": os.path.join(self.user_profile, "Documents"),
            "startup": os.path.join(
                os.environ.get('APPDATA', ''),
                'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
            ),
            "temp": os.environ.get('TEMP', ''),
            "desktop": os.path.join(self.user_profile, "Desktop"),
            "downloads": os.path.join(self.user_profile, "Downloads")
        }
        return paths.get(path_key, "")
