"""Console UI helpers for the Windows Automation Toolkit."""

import os
import sys


class ConsoleUIMixin:
    """Console rendering and interaction helpers."""

    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause_execution(self):
        """Pause execution and wait for user input"""
        input("\nPress Enter to continue...")

    def get_confirmation(self, message):
        """Get user confirmation for potentially risky operations. Default to 'yes' if Enter is pressed."""
        while True:
            response = input(f"\n{message} (Y/n): ").lower().strip()
            if response == '' or response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no")

    def print_header(self, title, subtitle=""):
        """Print a formatted header"""
        self.clear_screen()

        # Add padding on top
        print()

        # Display ASCII title centered
        ascii_title = [
            " ██████╗ ██╗    ██╗███████╗███╗   ██╗███████╗██╗   ██╗",
            "██╔═══██╗██║    ██║██╔════╝████╗  ██║╚══███╔╝╚██╗ ██╔╝",
            "██║   ██║██║ █╗ ██║█████╗  ██╔██╗ ██║  ███╔╝  ╚████╔╝ ",
            "██║▄▄ ██║██║███╗██║██╔══╝  ██║╚██╗██║ ███╔╝    ╚██╔╝  ",
            "╚██████╔╝╚███╔███╔╝███████╗██║ ╚████║███████╗   ██║   ",
            " ╚══▀▀═╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ",
            "                                                      "
        ]

        # Center each line of the ASCII title
        for line in ascii_title:
            print(line.center(100))
        print()

        # Display subtitle if provided
        if subtitle:
            print(subtitle.center(100))
            print()

    def print_menu(self, title, options):
        """Print a formatted menu with consistent left padding for better appearance"""
        # Calculate the width of the longest option
        max_option_length = len(title)
        for key, option in options.items():
            option_text = f"[{key}] {option.get('title', 'Unknown')}"
            max_option_length = max(max_option_length, len(option_text))

        # Pad to ensure minimum width
        max_option_length = max(max_option_length, 40)

        # Add consistent left padding (e.g., 10 spaces) for better visual appearance
        left_padding = " " * 5  # Add 5 spaces on the left for visual centering effect

        # Print title with left padding
        print(left_padding + title)
        print(left_padding + "-" * len(title))

        # Print each option with consistent left padding
        for key, option in options.items():
            option_text = f"[{key}] {option.get('title', 'Unknown')}"
            print(left_padding + option_text)

        print()

    def get_menu_choice(self, options):
        """Get and validate menu choice with single key press on Windows or input with Enter on other systems"""
        # Try to use Windows-specific input for single key press
        try:
            import msvcrt  # Windows-specific module

            print(f"Select option by pressing the number key: ", end="", flush=True)

            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8')
                    if key in options:
                        print(key)  # Echo the selected key
                        return key
                    elif key.lower() == 'q':  # Allow 'q' to quit
                        print("\nExiting...")
                        sys.exit(0)
                    else:
                        print(f"\n Invalid option '{key}'. Please try again.")
                        print(f"Select option by pressing the number key: ", end="", flush=True)
        except ImportError:
            # Fallback to regular input for non-Windows systems
            while True:
                choice = input("Select option by typing the number and pressing Enter: ").strip()
                if choice in options:
                    return choice
                else:
                    print(" Invalid option. Please try again.")
                    self.pause_execution()
