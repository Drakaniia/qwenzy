"""Action executors for the Textual interface."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile

from src.config.settings import AHK_SCRIPT_CONTENT, ULTIMATE_PERFORMANCE_GUID
from src.tui.models import ExecutionResult, ToolkitAction


class ToolkitActionExecutorMixin:
    """Execute toolkit actions and return UI-friendly results."""

    def run_action(self, action_id: str) -> ExecutionResult:
        """Execute an action by id."""
        action = self.find_action(action_id)
        try:
            if action.action_type == "open_setting":
                return self._open_setting(action)
            if action.action_type == "powershell_url":
                return self._run_powershell_url(action)
            if action.action_type == "install_optimization_app":
                return self._install_optimization_app(action)
            if action.action_type == "power_active":
                return self._run_powercfg(action, ["powercfg", "/getactivescheme"])
            if action.action_type == "power_list":
                return self._run_powercfg(action, ["powercfg", "-list"])
            if action.action_type == "power_unlock":
                return self._unlock_ultimate_performance(action)
            if action.action_type == "open_power_options":
                return self._open_setting(action)
            if action.action_type == "windows_optimization":
                return self._run_windows_optimization(action)
            if action.action_type == "automation_status":
                return self._automation_status_result(action)
            if action.action_type == "install_autohotkey":
                return self._install_autohotkey(action)
            if action.action_type == "create_autohotkey_startup":
                return self._create_autohotkey_startup(action)
        except Exception as exc:
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=False,
                message=f"{action.title} failed",
                details=str(exc),
            )

        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=False,
            message=f"No executor registered for {action.action_type}",
        )

    def _open_setting(self, action: ToolkitAction) -> ExecutionResult:
        command = action.payload.get("command", action.target)
        name = action.payload.get("name", action.title)
        success = self.settings.open_windows_tool(command, name)
        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=success,
            message=f"Opened {name}" if success else f"Could not open {name}",
            details=command,
        )

    def _run_powercfg(self, action: ToolkitAction, command: list[str]) -> ExecutionResult:
        success, output = self._run_subprocess(command, timeout=60)
        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=success,
            message=f"{action.title} completed" if success else f"{action.title} failed",
            details=output,
        )

    def _unlock_ultimate_performance(self, action: ToolkitAction) -> ExecutionResult:
        duplicate_success, duplicate_output = self._run_subprocess(
            ["powercfg", "-duplicatescheme", ULTIMATE_PERFORMANCE_GUID],
            timeout=60,
        )
        if not duplicate_success:
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=False,
                message="Could not create the Ultimate Performance plan",
                details=duplicate_output,
            )

        guid = self._extract_guid(duplicate_output)
        if not guid:
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=False,
                message="Power plan was created, but no GUID could be detected",
                details=duplicate_output,
            )

        activate_success, activate_output = self._run_subprocess(
            ["powercfg", "-setactive", guid],
            timeout=60,
        )
        details = "\n".join(part for part in [duplicate_output, activate_output] if part)
        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=activate_success,
            message=(
                f"Ultimate Performance plan activated: {guid}"
                if activate_success
                else f"Plan created but activation failed: {guid}"
            ),
            details=details,
        )

    def _run_windows_optimization(self, action: ToolkitAction) -> ExecutionResult:
        if not getattr(self.system, "is_admin", False):
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=False,
                message=f"{action.title} requires Administrator privileges",
                details=(
                    "Restart this app from an elevated PowerShell or Windows Terminal "
                    "session, then run the action again. This optimization uses "
                    "admin-only operations including restore points, HKLM registry "
                    "writes, netsh TCP settings, network adapter properties, powercfg, "
                    "and Windows service changes."
                ),
            )

        script = self.build_optimization_script(action)
        temp_script_path = ""

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".ps1", delete=False, encoding="utf-8") as temp_script:
                temp_script.write(script)
                temp_script_path = temp_script.name

            success, output = self._run_subprocess(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", temp_script_path],
                timeout=1200,
            )
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=success,
                message=f"{action.title} completed" if success else f"{action.title} failed",
                details=output,
            )
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                os.remove(temp_script_path)

    def _install_autohotkey(self, action: ToolkitAction) -> ExecutionResult:
        if self.autohotkey.check_autohotkey_installed():
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=True,
                message="AutoHotKey is already installed",
            )

        command = [
            "winget",
            "install",
            "--id",
            "AutoHotkey.AutoHotkey",
            "--accept-package-agreements",
            "--accept-source-agreements",
            "--silent",
        ]
        success, output = self._run_subprocess(command, timeout=300)
        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=success,
            message="AutoHotKey installation completed" if success else "AutoHotKey installation failed",
            details=output,
        )

    def _create_autohotkey_startup(self, action: ToolkitAction) -> ExecutionResult:
        ahk_dir = os.path.join(self.system.documents_folder, "AutoHotKey")
        os.makedirs(ahk_dir, exist_ok=True)

        script_path = os.path.join(ahk_dir, self.autohotkey.ahk_script_name)
        with open(script_path, "w", encoding="utf-8") as script_file:
            script_file.write(AHK_SCRIPT_CONTENT)

        startup_folder = self.system.get_system_path("startup")
        if not startup_folder:
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=False,
                message="Could not locate the Windows startup folder",
                details=script_path,
            )

        os.makedirs(startup_folder, exist_ok=True)
        startup_path = os.path.join(startup_folder, self.autohotkey.ahk_script_name)
        shutil.copy2(script_path, startup_path)

        details = f"Script: {script_path}\nStartup: {startup_path}"
        if self.autohotkey.check_autohotkey_installed() and not self.autohotkey.is_script_running():
            try:
                subprocess.Popen([self.autohotkey.ahk_executable, script_path])
                details += "\nScript launch requested."
            except Exception as exc:
                details += f"\nScript was created, but launch failed: {exc}"

        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=True,
            message="AutoHotKey script created and enabled for startup",
            details=details,
        )

    def _automation_status_result(self, action: ToolkitAction) -> ExecutionResult:
        installed = self.autohotkey.check_autohotkey_installed()
        script_path = self.autohotkey.get_script_path()
        script_exists = os.path.exists(script_path)
        running = self.autohotkey.is_script_running() if installed else False
        startup_folder = self.system.get_system_path("startup")
        startup_path = os.path.join(startup_folder, self.autohotkey.ahk_script_name) if startup_folder else ""
        startup_enabled = bool(startup_path and os.path.exists(startup_path))

        details = "\n".join(
            [
                f"AutoHotKey installed: {'Yes' if installed else 'No'}",
                f"Script exists: {'Yes' if script_exists else 'No'}",
                f"Script running: {'Yes' if running else 'No'}",
                f"Startup enabled: {'Yes' if startup_enabled else 'No'}",
                f"Script path: {script_path}",
            ]
        )

        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=True,
            message="AutoHotKey status refreshed",
            details=details,
        )

    def _install_optimization_app(self, action: ToolkitAction) -> ExecutionResult:
        install_methods = action.payload["script"]["install_methods"]
        if self.system.check_chocolatey_available():
            command: str | list[str] = install_methods["choco"]
        elif self.system.check_winget_available():
            command = install_methods["winget"]
        else:
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=False,
                message="No supported package manager is available",
                details="Install winget or Chocolatey first.",
            )

        success, output = self._run_subprocess(command, timeout=300, shell=True)
        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=success,
            message=(
                f"{action.title} installation completed"
                if success
                else f"{action.title} installation failed"
            ),
            details=output,
        )

    def _run_powershell_url(self, action: ToolkitAction) -> ExecutionResult:
        url = action.payload["url"]
        ps_command = self._powershell_command_for_url(url)
        temp_script_path = ""

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".ps1", delete=False, encoding="utf-8") as temp_script:
                temp_script.write(f"{ps_command}\n")
                temp_script_path = temp_script.name

            success, output = self._run_subprocess(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_script_path],
                timeout=600,
            )
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=success,
                message=f"{action.title} completed" if success else f"{action.title} failed",
                details=output,
            )
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                os.remove(temp_script_path)

    def _powershell_command_for_url(self, url: str) -> str:
        if "get.activated.win" in url:
            return f"irm {url} | iex"
        if "debloat.raphi.re" in url:
            return f"& ([scriptblock]::Create((irm \"{url}\")))"
        if "christitus.com/win" in url:
            return f"iwr -useb {url} | iex"
        if "git.io/debloat11" in url:
            return f"iwr {url}|iex"
        return f"[scriptblock]::Create((irm \"{url}\"))"

    def _run_subprocess(
        self,
        command: str | list[str],
        *,
        timeout: int,
        shell: bool = False,
    ) -> tuple[bool, str]:
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except FileNotFoundError as exc:
            return False, str(exc)
        except subprocess.TimeoutExpired as exc:
            output = "\n".join(part for part in [exc.stdout, exc.stderr] if part)
            return False, f"Command timed out after {timeout} seconds.\n{output}".strip()

        output = "\n".join(part.strip() for part in [result.stdout, result.stderr] if part and part.strip())
        return result.returncode == 0, output

    def _extract_guid(self, output: str) -> str | None:
        match = re.search(
            r"\{?[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}?",
            output,
        )
        return match.group(0) if match else None
