"""
System utilities for Windows Automation Toolkit
"""

import ctypes
import os
import sys

from src.utils.filesystem import FileSystemMixin
from src.utils.package_manager import PackageManagerMixin
from src.utils.powershell import PowerShellMixin
from src.utils.ui import ConsoleUIMixin


class SystemUtils(ConsoleUIMixin, PowerShellMixin, PackageManagerMixin, FileSystemMixin):
    """Core system utilities for Windows automation"""

    def __init__(self):
        self.is_admin = self.check_admin_privileges()
        self.user_profile = os.path.expanduser("~")
        self.documents_folder = os.path.join(self.user_profile, "Documents")

    def check_admin_privileges(self):
        """Check if the script is running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def relaunch_as_admin(self):
        """Relaunch the script with administrator privileges"""
        if not self.is_admin:
            try:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit(0)
            except Exception as e:
                print(f" Failed to relaunch as admin: {e}")
                return False
        return True
