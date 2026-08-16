"""Command-line entry point for the Windows Automation Toolkit."""

from src.tui.app import WindowsToolkitApp


def main() -> None:
    """Run the Textual user interface."""
    WindowsToolkitApp().run()


if __name__ == "__main__":
    main()
