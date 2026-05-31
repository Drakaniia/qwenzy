#!/usr/bin/env python3
"""
Windows Automation Toolkit - Textual Entry Point.
"""

from src.tui.app import WindowsToolkitApp


def main() -> None:
    """Run the Textual user interface."""
    WindowsToolkitApp().run()


if __name__ == "__main__":
    main()
