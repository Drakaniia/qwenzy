"""Package manager (winget / Chocolatey) detection and installation helpers."""

import subprocess


class PackageManagerMixin:
    """winget and Chocolatey availability checks and installers."""

    def check_winget_available(self):
        """Check if winget is available on the system"""
        return self.check_program_exists("winget")

    def check_chocolatey_available(self):
        """Check if Chocolatey is available on the system"""
        return self.check_program_exists("choco")

    def install_winget(self):
        """Install Windows Package Manager (winget)"""
        self.clear_screen()
        self.print_header("Install Windows Package Manager (winget)")

        print(" Winget is the official Windows package manager from Microsoft.")
        print(" It's required for installing applications in this toolkit.")
        print()
        print(" Installation method:")
        print(" - Downloads winget from Microsoft's official source")
        print(" - Requires internet connection")
        print()

        if not self.get_confirmation("Install winget now?"):
            print(" Installation cancelled by user")
            return False

        print("\n Installing winget...")
        print("-" * 50)

        # PowerShell command to install winget from Microsoft
        install_command = '''
        $ErrorActionPreference = "Stop"
        Write-Host "Downloading winget..."

        # Try to install via the Microsoft winget package
        try {
            # Method 1: Install from Microsoft Store (if available)
            Start-Process "ms-windows-store://pdp/?ProductId=9NBLGGH4NNS1" -Wait
            Write-Host "Please install Windows Package Manager from Microsoft Store"
        }
        catch {
            Write-Host "Microsoft Store method failed, trying direct download..."
        }

        # Method 2: Direct download of winget CLI
        $wingetUrl = "https://aka.ms/winget"
        Write-Host "Opening winget download page: $wingetUrl"
        Start-Process $wingetUrl

        Write-Host ""
        Write-Host "Please download and install winget from the opened page."
        Write-Host "After installation, restart this toolkit."
        '''

        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", install_command],
                capture_output=True,
                text=True,
                timeout=120
            )
            print(result.stdout)
            if result.stderr:
                print(result.stderr)

            print("\nℹ️ Winget installation may require a system restart.")
            print(" After installation completes, please restart this toolkit.")
            return True

        except subprocess.TimeoutExpired:
            print(" Installation timed out")
            return False
        except Exception as e:
            print(f" Error installing winget: {e}")
            return False

    def install_chocolatey(self):
        """Install Chocolatey package manager"""
        self.clear_screen()
        self.print_header("Install Chocolatey Package Manager")

        print(" Chocolatey is a popular package manager for Windows.")
        print(" It provides an alternative to winget for installing applications.")
        print()
        print(" Installation method:")
        print(" - Official Chocolatey installation script")
        print(" - Requires internet connection and admin privileges")
        print()

        if not self.get_confirmation("Install Chocolatey now?"):
            print(" Installation cancelled by user")
            return False

        print("\n Installing Chocolatey...")
        print("-" * 50)

        # Official Chocolatey installation command
        install_command = '''
        $ErrorActionPreference = "Stop"
        Set-ExecutionPolicy Bypass -Scope Process -Force

        Write-Host "Downloading Chocolatey installer..."
        $chocoInstaller = Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

        Write-Host "Installing Chocolatey..."
        & $chocoInstaller

        Write-Host ""
        Write-Host "Chocolatey installation completed!"
        Write-Host "Run 'choco --version' to verify installation."
        '''

        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", install_command],
                capture_output=True,
                text=True,
                timeout=300
            )
            print(result.stdout)
            if result.stderr:
                print(result.stderr)

            if result.returncode == 0:
                print("\n Chocolatey installed successfully!")
                return True
            else:
                print("\n Chocolatey installation may have encountered issues.")
                print(" Please check the output above for details.")
                return False

        except subprocess.TimeoutExpired:
            print(" Installation timed out")
            return False
        except Exception as e:
            print(f" Error installing Chocolatey: {e}")
            return False

    def ensure_package_manager(self, preferred="winget"):
        """
        Ensure at least one package manager is available.
        Returns: tuple (available_manager, was_installed)
        - available_manager: 'winget', 'choco', or None
        - was_installed: True if we installed a manager, False if already available
        """
        winget_available = self.check_winget_available()
        choco_available = self.check_chocolatey_available()

        # If preferred is available, use it
        if preferred == "winget" and winget_available:
            return "winget", False
        if preferred == "choco" and choco_available:
            return "choco", False

        # If either is available, use it
        if winget_available:
            return "winget", False
        if choco_available:
            return "choco", False

        # Neither is available, offer to install
        self.clear_screen()
        self.print_header("Package Manager Required")

        print(" No package manager (winget or Chocolatey) is installed.")
        print(" Package managers are required to install applications.")
        print()
        print(" Available options:")
        print(" [1] Install winget (Microsoft's official package manager)")
        print(" [2] Install Chocolatey (Popular community package manager)")
        print(" [0] Cancel")
        print()

        choice = input(" Enter your choice (0-2): ").strip()

        if choice == "1":
            if self.install_winget():
                print("\n Winget installation initiated.")
                print(" Please restart the toolkit after installation completes.")
                self.pause_execution()
                return None, True
        elif choice == "2":
            if self.install_chocolatey():
                print("\n Chocolatey installed successfully!")
                return "choco", True

        return None, True
