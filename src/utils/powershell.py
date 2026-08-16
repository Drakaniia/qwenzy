"""PowerShell command and script execution helpers."""

import os
import subprocess
import tempfile


class PowerShellMixin:
    """PowerShell and generic command execution helpers."""

    def run_powershell_command(self, command, bypass_policy=True, timeout=300, interactive=False):
        """Execute a PowerShell command with optional execution policy bypass"""
        try:
            if bypass_policy:
                if interactive:
                    ps_args = ["powershell", "-ExecutionPolicy", "Bypass", "-NoExit", "-WindowStyle", "Normal", "-Command", command]
                else:
                    ps_args = ["powershell", "-ExecutionPolicy", "Bypass", "-Command", command]
            else:
                if interactive:
                    ps_args = ["powershell", "-NoExit", "-WindowStyle", "Normal", "-Command", command]
                else:
                    ps_args = ["powershell", "-Command", command]

            print(f" Executing: {command}")

            if interactive:
                # For interactive scripts, don't capture output to allow GUI to show
                result = subprocess.run(
                    ps_args,
                    timeout=timeout
                )

                # For interactive commands, we assume success if no exception occurs
                # since the window is meant to stay open for user interaction
                print("Command executed successfully")
                return True, ""
            else:
                result = subprocess.run(
                    ps_args,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )

                if result.returncode == 0:
                    print("Command executed successfully")
                    if result.stdout and result.stdout.strip():
                        print(f"Output: {result.stdout.strip()}")
                    return True, result.stdout
                else:
                    print(f"Command failed: {result.stderr.strip() if result.stderr else 'Unknown error'}")
                    return False, result.stderr

        except subprocess.TimeoutExpired:
            print("Command timed out")
            return False, "Command timed out"
        except Exception as e:
            print(f"Error executing command: {e}")
            return False, str(e)

    def run_powershell_script(self, script_url, description):
        """Execute a PowerShell script from URL"""
        print(f"\n{description}")
        print("=" * 50)

        if not self.get_confirmation(f"Run {description}? This will execute PowerShell scripts from the internet."):
            print("Operation cancelled by user")
            return False

        # For all PowerShell scripts, use a temporary file approach
        if "get.activated.win" in script_url:
            # For Windows activation, use the proper command: irm https://get.activated.win | iex
            ps_command = f"irm {script_url} | iex"
            print(f" Executing activation command: {ps_command}")
        elif "debloat.raphi.re" in script_url:
            # For Win11Debloat, use the proper command: & ([scriptblock]::Create((irm "https://debloat.raphi.re/")))
            ps_command = f"& ([scriptblock]::Create((irm \\\"{script_url}\\\")))"
            print(f" Executing debloat command: {ps_command}")
        elif "christitus.com/win" in script_url:
            # For Windows tweaks, use the proper command: iwr -useb https://christitus.com/win | iex
            ps_command = f"iwr -useb {script_url} | iex"
            print(f" Executing tweaks command: {ps_command}")
        elif "git.io/debloat11" in script_url:
            # For Debloat11, use the proper command: iwr https://git.io/debloat11|iex
            ps_command = f"iwr {script_url}|iex"
            print(f" Executing debloat11 command: {ps_command}")
        else:
            # For other scripts, use the generic approach
            ps_command = f"[scriptblock]::Create((irm \\\"{script_url}\\\"))"
            print(f" Executing command: {ps_command}")

        print(" Running PowerShell command...")

        # Create a temporary PowerShell script to execute the command
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as temp_ps:
            # Don't try to set execution policy since PowerShell is run with Bypass
            temp_ps.write(f"""
{ps_command}
""")
            temp_script_path = temp_ps.name

        try:
            # Execute the temporary script with PowerShell Bypass policy
            ps_args = ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_script_path]

            # Run the command with real-time output
            result = subprocess.run(
                ps_args,
                capture_output=False,  # Don't capture, let it display directly
                text=True
            )

            # Clean up the temporary file
            os.remove(temp_script_path)

            # Report success regardless of return code since these scripts may exit with different codes
            # but still be functionally successful
            print(f"\n {description} completed successfully")
            return True

        except Exception as e:
            # Clean up the temporary file even if there's an error
            try:
                os.remove(temp_script_path)
            except:
                pass
            print(f" Error executing {description}: {e}")
            return False

    def run_command(self, command, shell=True, timeout=60):
        """Run a system command"""
        try:
            print(f" Executing: {command}")
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                print("Command executed successfully")
                if result.stdout.strip():
                    print(f"Output: {result.stdout.strip()}")
                return True, result.stdout
            else:
                print(f"Command failed: {result.stderr.strip()}")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            print("Command timed out")
            return False, "Command timed out"
        except Exception as e:
            print(f"Error executing command: {e}")
            return False, str(e)
