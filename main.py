#!/usr/bin/env python3
"""
Windows Automation Toolkit - Main Entry Point
A comprehensive Windows 10/11 optimization and productivity toolkit
Author: AI Assistant
Version: 2.0.0 - Modular Architecture
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.system import SystemUtils
from src.modules.debloat import WindowsDebloat
from src.modules.settings import WindowsSettings
from src.modules.power import PowerManagement
from src.modules.installer import AppInstaller
from src.modules.ai_tools import AIToolsInstaller
from src.modules.autohotkey import AutoHotKeyManager
from src.config.settings import UI_CONFIG


class WindowsAutomationToolkit:
    """Main Windows Automation Toolkit class"""
    
    def __init__(self):
        self.system = SystemUtils()
        self.debloat = WindowsDebloat(self.system)
        self.settings = WindowsSettings(self.system)
        self.power = PowerManagement(self.system)
        self.installer = AppInstaller(self.system)
        self.ai_tools = AIToolsInstaller(self.system)
        self.autohotkey = AutoHotKeyManager(self.system)
    
    def run(self):
        """Main entry point for the toolkit"""
        # Check admin privileges and relaunch if needed
        if not self.system.is_admin:
            print("This toolkit requires administrator privileges for full functionality.")
            if self.system.get_confirmation("Relaunch as Administrator?"):
                if self.system.relaunch_as_admin():
                    return
            else:
                print("Some features may not work without administrator privileges.")
                self.system.pause_execution()

        # Display ASCII title
        self.system.clear_screen()
        print(" ██████╗ ██╗    ██╗███████╗███╗   ██╗███████╗██╗   ██╗")
        print("██╔═══██╗██║    ██║██╔════╝████╗  ██║╚══███╔╝╚██╗ ██╔╝")
        print("██║   ██║██║ █╗ ██║█████╗  ██╔██╗ ██║  ███╔╝  ╚████╔╝ ")
        print("██║▄▄ ██║██║███╗██║██╔══╝  ██║╚██╗██║ ███╔╝    ╚██╔╝  ")
        print("╚██████╔╝╚███╔███╔╝███████╗██║ ╚████║███████╗   ██║   ")
        print(" ╚══▀▀═╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ")
        print("                                                      ")
        print()
        self.system.pause_execution()

        # Start the main menu
        self.main_menu()
    
    def main_menu(self):
        """Display the main menu and handle user input"""
        while True:
            self.system.print_header(
                UI_CONFIG["header_title"], 
                UI_CONFIG["header_subtitle"]
            )
            
            self.system.print_menu("MAIN MENU", UI_CONFIG["menu_options"])
            
            choice = self.system.get_menu_choice(UI_CONFIG["menu_options"])

            if choice == "1":
                self.debloat.show_debloat_menu()
            elif choice == "2":
                self.settings.show_settings_menu()
            elif choice == "3":
                self.power.show_power_menu()
            elif choice == "4":
                self.installer.show_installer_menu()
            elif choice == "5":
                self.ai_tools.show_ai_tools_menu()
            elif choice == "6":
                self.autohotkey.show_autohotkey_menu()
            elif choice == "0":
                self.exit_toolkit()
                break

    def exit_toolkit(self):
        """Exit the toolkit with a farewell message"""
        self.system.clear_screen()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                     THANK YOU FOR USING!                   ║")
        print("║              Windows Automation Toolkit v2.0.0                ║")
        print("║                                                              ║")
        print("║  Your Windows system has been optimized and enhanced!        ║")
        print("║                                                              ║")
        print("║  Productivity Boosted!                                       ║")
        print("║  Performance Optimized!                                      ║")
        print("║  System Secured!                                             ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        print("Goodbye and enjoy your optimized Windows experience!")
    
    def show_system_info(self):
        """Display system information"""
        self.system.clear_screen()
        self.system.print_header("System Information")
        
        print(" System Details:")
        print("=" * 40)
        print(f" User: {self.system.user_profile}")
        print(f" Documents: {self.system.documents_folder}")
        print(f"Admin: {'Yes' if self.system.is_admin else 'No'}")
        
        # Check available tools
        print("\n Available Tools:")
        print("-" * 40)
        print(f"Winget: {'Available' if self.system.check_program_exists('winget') else 'Not Available'}")
        print(f"Node.js: {'Available' if self.system.check_program_exists('node') else 'Not Available'}")
        print(f"npm: {'Available' if self.system.check_program_exists('npm') else 'Not Available'}")
        print(f"AutoHotKey: {'Available' if self.system.check_program_exists('AutoHotkey64.exe') else 'Not Available'}")
        
        self.system.pause_execution()


def main():
    """Main function"""
    try:
        toolkit = WindowsAutomationToolkit()
        toolkit.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()