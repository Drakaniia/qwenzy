"""Business-facing service layer for the Textual interface."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from typing import Any

from src.config.settings import (
    AHK_SCRIPT_CONTENT,
    POWERSHELL_SCRIPTS,
    ULTIMATE_PERFORMANCE_GUID,
    WINDOWS_COMMANDS,
    WINDOWS_OPTIMIZATION_ACTIONS,
)
from src.modules.autohotkey import AutoHotKeyManager
from src.modules.power import PowerManagement
from src.modules.settings import WindowsSettings
from src.utils.system import SystemUtils


@dataclass(frozen=True)
class ToolkitAction:
    """A structured command the TUI can render and execute."""

    id: str
    section: str
    title: str
    target: str
    description: str
    action_type: str
    risk: str = "Low"
    status: str = "Ready"
    requires_confirmation: bool = False
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolkitSection:
    """A group of related toolkit actions."""

    id: str
    title: str
    description: str
    actions: list[ToolkitAction]


@dataclass(frozen=True)
class ExecutionResult:
    """Result returned after running a toolkit action."""

    action_id: str
    title: str
    success: bool
    message: str
    details: str = ""


class ToolkitActionService:
    """Expose existing toolkit behavior as UI-neutral actions."""

    def __init__(
        self,
        system: SystemUtils | None = None,
        *,
        probe_tools: bool = True,
    ) -> None:
        self.system = system or SystemUtils()
        self.probe_tools = probe_tools
        self.settings = WindowsSettings(self.system)
        self.power = PowerManagement(self.system)
        self.autohotkey = AutoHotKeyManager(self.system)

    def get_sections(self) -> list[ToolkitSection]:
        """Return the current action catalog."""
        return [
            self._debloat_section(),
            self._optimization_section(),
            self._settings_section(),
            self._power_section(),
            self._automation_section(),
        ]

    def get_overview(self) -> list[tuple[str, str, str]]:
        """Return compact system status cards for the UI."""
        return [
            ("Admin", "Ready" if self.system.is_admin else "Limited", "Elevated session detected" if self.system.is_admin else "Some actions need administrator rights"),
            ("Winget", self._tool_status("winget"), "Required for package-managed toolkit actions"),
            ("AutoHotKey", self._autohotkey_status(), "Automation script runtime"),
        ]

    def find_action(self, action_id: str) -> ToolkitAction:
        """Find an action by id or raise KeyError."""
        for section in self.get_sections():
            for action in section.actions:
                if action.id == action_id:
                    return action
        raise KeyError(action_id)

    def filter_actions(self, query: str) -> list[ToolkitSection]:
        """Return sections with actions matching a user query."""
        normalized_query = query.strip().lower()
        if not normalized_query:
            return self.get_sections()

        sections: list[ToolkitSection] = []
        for section in self.get_sections():
            actions = [
                action
                for action in section.actions
                if normalized_query in " ".join(
                    [
                        action.title,
                        action.target,
                        action.description,
                        action.risk,
                        action.status,
                    ]
                ).lower()
            ]
            sections.append(
                ToolkitSection(
                    id=section.id,
                    title=section.title,
                    description=section.description,
                    actions=actions,
                )
            )
        return sections

    def run_action(self, action_id: str) -> ExecutionResult:
        """Execute an action by id."""
        action = self.find_action(action_id)
        try:
            if action.action_type == "open_setting":
                return self._open_setting(action)
            if action.action_type == "powershell_url":
                return self._run_powershell_url(action)
            if action.action_type == "memory_cleaner":
                return self._install_memory_cleaner(action)
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

    def _debloat_section(self) -> ToolkitSection:
        actions: list[ToolkitAction] = []

        for category, scripts in POWERSHELL_SCRIPTS.items():
            for key, script in scripts.items():
                if category == "memory_cleaner":
                    actions.append(
                        ToolkitAction(
                            id=f"debloat.{category}.{key}",
                            section="debloat",
                            title=script["name"],
                            target="winget or Chocolatey",
                            description=script["description"],
                            action_type="memory_cleaner",
                            risk="Medium",
                            requires_confirmation=True,
                            payload={"script": script},
                        )
                    )
                    continue

                actions.append(
                    ToolkitAction(
                        id=f"debloat.{category}.{key}",
                        section="debloat",
                        title=script["name"],
                        target=script["url"],
                        description=script["description"],
                        action_type="powershell_url",
                        risk="High",
                        requires_confirmation=True,
                        payload={"url": script["url"]},
                    )
                )

        return ToolkitSection(
            id="debloat",
            title="Debloat",
            description="Run curated Windows cleanup, tweak, and activation scripts.",
            actions=actions,
        )

    def _optimization_section(self) -> ToolkitSection:
        actions = [
            ToolkitAction(
                id=f"optimization.{item['id']}",
                section="optimization",
                title=item["title"],
                target=item["target"],
                description=item["description"],
                action_type="windows_optimization",
                risk=item["risk"],
                requires_confirmation=True,
                payload={"groups": item["groups"]},
            )
            for item in WINDOWS_OPTIMIZATION_ACTIONS
        ]

        return ToolkitSection(
            id="optimization",
            title="Optimization",
            description="Apply OPTIMIZE.md Windows 10/11 settings automatically with generated PowerShell.",
            actions=actions,
        )

    def _settings_section(self) -> ToolkitSection:
        display_names = {
            "performance": "Performance Options",
            "system": "System Properties",
            "power": "Power Options",
            "network": "Network Connections",
        }
        actions = [
            ToolkitAction(
                id=f"settings.{key}",
                section="settings",
                title=display_names.get(key, key.replace("_", " ").title()),
                target=command,
                description=f"Open {display_names.get(key, key)} with the Windows Run command.",
                action_type="open_setting",
                payload={"command": command, "name": display_names.get(key, key)},
            )
            for key, command in WINDOWS_COMMANDS.items()
        ]

        return ToolkitSection(
            id="settings",
            title="Settings",
            description="Open common Windows control panels and system tools.",
            actions=actions,
        )

    def _power_section(self) -> ToolkitSection:
        return ToolkitSection(
            id="power",
            title="Power",
            description="Inspect and tune Windows power plans.",
            actions=[
                ToolkitAction(
                    id="power.active",
                    section="power",
                    title="Show Active Power Plan",
                    target="powercfg /getactivescheme",
                    description="Display the currently active power profile.",
                    action_type="power_active",
                ),
                ToolkitAction(
                    id="power.list",
                    section="power",
                    title="List Power Plans",
                    target="powercfg -list",
                    description="Show every registered power scheme.",
                    action_type="power_list",
                ),
                ToolkitAction(
                    id="power.unlock",
                    section="power",
                    title="Unlock Ultimate Performance",
                    target=ULTIMATE_PERFORMANCE_GUID,
                    description="Create and activate the Ultimate Performance plan.",
                    action_type="power_unlock",
                    risk="Medium",
                    requires_confirmation=True,
                ),
                ToolkitAction(
                    id="power.options",
                    section="power",
                    title="Open Power Options",
                    target=WINDOWS_COMMANDS["power"],
                    description="Open the Windows Power Options control panel.",
                    action_type="open_power_options",
                    payload={"command": WINDOWS_COMMANDS["power"], "name": "Power Options"},
                ),
            ],
        )

    def _automation_section(self) -> ToolkitSection:
        return ToolkitSection(
            id="automation",
            title="Automation",
            description="Install AutoHotKey and manage the toolkit script.",
            actions=[
                ToolkitAction(
                    id="automation.status",
                    section="automation",
                    title="Show AutoHotKey Status",
                    target="AutoHotKey runtime and startup script",
                    description="Check whether AutoHotKey and the automation script are ready.",
                    action_type="automation_status",
                    status=self._autohotkey_status(),
                ),
                ToolkitAction(
                    id="automation.install",
                    section="automation",
                    title="Install AutoHotKey",
                    target="AutoHotkey.AutoHotkey",
                    description="Install AutoHotKey through winget.",
                    action_type="install_autohotkey",
                    risk="Medium",
                    status=self._tool_status("winget"),
                    requires_confirmation=True,
                ),
                ToolkitAction(
                    id="automation.create_startup",
                    section="automation",
                    title="Create Script and Enable Startup",
                    target="Documents\\AutoHotKey\\automation.ahk",
                    description="Create the default script and copy it into the Windows startup folder.",
                    action_type="create_autohotkey_startup",
                    risk="Medium",
                    requires_confirmation=True,
                ),
            ],
        )

    def _tool_status(self, executable: str) -> str:
        if not self.probe_tools:
            return "Not checked"
        return "Available" if self.system.check_program_exists(executable) else "Missing"

    def _autohotkey_status(self) -> str:
        if not self.probe_tools:
            return "Not checked"
        return "Installed" if self.autohotkey.check_autohotkey_installed() else "Missing"

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

    def build_optimization_script(self, action: ToolkitAction) -> str:
        """Build the PowerShell script for a Windows optimization action."""
        groups = action.payload.get("groups", [])
        blocks = self._optimization_script_blocks()
        selected_blocks = [blocks[group] for group in groups if group in blocks]

        prelude = r'''
# Generated by Windows Automation Toolkit.
$ErrorActionPreference = "Continue"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "== $Message ==" -ForegroundColor Cyan
}

function Set-RegistryDword {
    param(
        [string]$Path,
        [string]$Name,
        [int]$Value
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -Path $Path -Force | Out-Null
    }
    New-ItemProperty -Path $Path -Name $Name -Value $Value -PropertyType DWord -Force | Out-Null
}

function Set-RegistryString {
    param(
        [string]$Path,
        [string]$Name,
        [string]$Value
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -Path $Path -Force | Out-Null
    }
    New-ItemProperty -Path $Path -Name $Name -Value $Value -PropertyType String -Force | Out-Null
}

function Remove-ContentsIfPresent {
    param([string[]]$Paths)
    foreach ($Path in $Paths) {
        $ExpandedPath = [Environment]::ExpandEnvironmentVariables($Path)
        if (Test-Path -LiteralPath $ExpandedPath) {
            Write-Host "Cleaning $ExpandedPath"
            Get-ChildItem -LiteralPath $ExpandedPath -Force -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

function Disable-ServiceIfPresent {
    param([string[]]$Names)
    foreach ($Name in $Names) {
        $Service = Get-Service -Name $Name -ErrorAction SilentlyContinue
        if ($Service) {
            Write-Host "Disabling service $Name"
            Stop-Service -Name $Name -Force -ErrorAction SilentlyContinue
            Set-Service -Name $Name -StartupType Disabled -ErrorAction SilentlyContinue
        }
    }
}

$Principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $Principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Run this action as Administrator so every optimization can be applied."
}
'''
        footer = r'''
Write-Step "Optimization complete"
Write-Host "Restart Windows to let all service, registry, and power changes take effect."
'''
        return "\n".join([prelude.strip(), *selected_blocks, footer.strip(), ""])

    def _run_windows_optimization(self, action: ToolkitAction) -> ExecutionResult:
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

    def _optimization_script_blocks(self) -> dict[str, str]:
        return {
            "restore_point": r'''
Write-Step "Create restore point"
try {
    Enable-ComputerRestore -Drive "$env:SystemDrive\" -ErrorAction SilentlyContinue
    Checkpoint-Computer -Description "Before Windows Automation Toolkit optimization" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop
} catch {
    Write-Warning "Restore point could not be created: $($_.Exception.Message)"
}
'''.strip(),
            "cleanup": r'''
Write-Step "Disk cleanup"
Stop-Service -Name wuauserv,bits -Force -ErrorAction SilentlyContinue
Remove-ContentsIfPresent @(
    "%TEMP%",
    "$env:WINDIR\Temp",
    "$env:WINDIR\Prefetch",
    "$env:WINDIR\SoftwareDistribution\Download",
    "$env:ProgramData\NVIDIA Corporation\Downloader",
    "$env:ProgramFiles\NVIDIA Corporation\Installer2"
)
Start-Service -Name wuauserv,bits -ErrorAction SilentlyContinue
Start-Process -FilePath "wsreset.exe" -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue
'''.strip(),
            "network": r'''
Write-Step "Network throughput and adapter power saving"
netsh int tcp set global autotuninglevel=disabled
netsh int tcp set supplemental template=internet congestionprovider=ctcp
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Psched" "NonBestEffortLimit" 0

$AdapterTweaks = @(
    "Energy Efficient Ethernet",
    "Energy Efficient Ethernet (EEE)",
    "Advanced EEE",
    "Gigabit Lite",
    "Green Ethernet",
    "Power Saving Mode",
    "Selective Suspend"
)
foreach ($Adapter in Get-NetAdapter -Physical -ErrorAction SilentlyContinue) {
    foreach ($DisplayName in $AdapterTweaks) {
        Set-NetAdapterAdvancedProperty -Name $Adapter.Name -DisplayName $DisplayName -DisplayValue "Disabled" -NoRestart -ErrorAction SilentlyContinue
    }

    $PowerCommand = Get-Command Set-NetAdapterPowerManagement -ErrorAction SilentlyContinue
    if ($PowerCommand) {
        $PowerParams = @{ Name = $Adapter.Name; ErrorAction = "SilentlyContinue" }
        foreach ($ParamName in @("AllowComputerToTurnOffDevice", "DeviceSleepOnDisconnect", "WakeOnMagicPacket", "WakeOnPattern", "SelectiveSuspend")) {
            if ($PowerCommand.Parameters.Keys -contains $ParamName) {
                $PowerParams[$ParamName] = "Disabled"
            }
        }
        Set-NetAdapterPowerManagement @PowerParams
    }
}
'''.strip(),
            "performance": rf'''
Write-Step "Power, gaming, storage, and peripheral performance"
$UltimateGuid = "{ULTIMATE_PERFORMANCE_GUID}"
$DuplicateOutput = powercfg -duplicatescheme $UltimateGuid 2>&1
$CreatedGuid = [regex]::Match(($DuplicateOutput | Out-String), "[0-9a-fA-F]{{8}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{12}}").Value
if ($CreatedGuid) {{
    powercfg -setactive $CreatedGuid
}} else {{
    powercfg -setactive "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
}}
powercfg /hibernate off

Set-RegistryDword "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" "HwSchMode" 2
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\StorageSense\Parameters\StoragePolicy" "01" 0
Set-RegistryDword "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" "fDenyTSConnections" 1
Set-RegistryDword "HKCU:\Software\Microsoft\Clipboard" "EnableClipboardHistory" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Clipboard" "CloudClipboardAutomaticUpload" 0
Set-RegistryDword "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config" "DODownloadMode" 0
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization" "DODownloadMode" 0

Set-RegistryDword "HKCU:\System\GameConfigStore" "GameDVR_Enabled" 0
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\GameDVR" "AllowGameDVR" 0
Set-RegistryDword "HKCU:\Software\Microsoft\GameBar" "AllowAutoGameMode" 1
Set-RegistryDword "HKCU:\Software\Microsoft\GameBar" "AutoGameModeEnabled" 1
Set-RegistryDword "HKCU:\Software\Microsoft\GameBar" "ShowStartupPanel" 0
Set-RegistryDword "HKCU:\Software\Microsoft\GameBar" "GameMode" 1

Set-RegistryString "HKCU:\Control Panel\Mouse" "MouseSpeed" "0"
Set-RegistryString "HKCU:\Control Panel\Mouse" "MouseThreshold1" "0"
Set-RegistryString "HKCU:\Control Panel\Mouse" "MouseThreshold2" "0"
Set-RegistryString "HKCU:\Control Panel\Mouse" "DoubleClickSpeed" "200"
Set-RegistryString "HKCU:\Control Panel\Accessibility\StickyKeys" "Flags" "506"
Set-RegistryString "HKCU:\Control Panel\Accessibility\Keyboard Response" "Flags" "122"
Set-RegistryString "HKCU:\Control Panel\Accessibility\ToggleKeys" "Flags" "58"
'''.strip(),
            "privacy": r'''
Write-Step "Privacy, telemetry, activity, and app permissions"
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo" "Enabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Privacy" "TailoredExperiencesWithDiagnosticDataEnabled" 0
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" "AllowTelemetry" 1
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" "DisableTailoredExperiencesWithDiagnosticData" 1
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\System" "PublishUserActivities" 0
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\System" "UploadUserActivities" 0
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors" "DisableLocation" 1
Set-RegistryString "HKCU:\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location" "Value" "Deny"
Set-RegistryDword "HKCU:\Software\Microsoft\Speech_OneCore\Settings\OnlineSpeechPrivacy" "HasAccepted" 0
Set-RegistryDword "HKCU:\Software\Microsoft\InputPersonalization" "RestrictImplicitTextCollection" 1
Set-RegistryDword "HKCU:\Software\Microsoft\InputPersonalization" "RestrictImplicitInkCollection" 1
Set-RegistryDword "HKCU:\Software\Microsoft\InputPersonalization\TrainedDataStore" "HarvestContacts" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" "GlobalUserDisabled" 1

foreach ($Permission in @("webcam", "microphone", "location", "appDiagnostics", "userNotificationListener", "contacts", "appointments", "phoneCall", "radios", "bluetoothSync")) {
    Set-RegistryString "HKCU:\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\$Permission" "Value" "Deny"
}
'''.strip(),
            "interface": r'''
Write-Step "Explorer, Start, taskbar, tips, suggestions, and accessibility launchers"
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" "LaunchTo" 1
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer" "ShowRecent" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer" "ShowFrequent" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" "Start_TrackProgs" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" "Start_TrackDocs" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" "Start_ShowRecentlyAddedApps" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Search" "SearchboxTaskbarMode" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" "ShowTaskViewButton" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" "NoInstrumentation" 1

Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "ContentDeliveryAllowed" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "FeatureManagementEnabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "OemPreInstalledAppsEnabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "PreInstalledAppsEnabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "SilentInstalledAppsEnabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "SoftLandingEnabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "SubscribedContent-338388Enabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "SubscribedContent-338389Enabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "SubscribedContent-353698Enabled" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" "SystemPaneSuggestionsEnabled" 0
Set-RegistryDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\CloudContent" "DisableWindowsConsumerFeatures" 1

Set-RegistryDword "HKCU:\Software\Microsoft\ScreenMagnifier" "RunningState" 0
Set-RegistryDword "HKCU:\Software\Microsoft\Narrator\NoRoam" "WinEnterLaunchEnabled" 0
Remove-Item "$env:APPDATA\Microsoft\Windows\Recent\*" -Recurse -Force -ErrorAction SilentlyContinue
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
Start-Process explorer.exe
'''.strip(),
            "services": r'''
Write-Step "Optional service optimization"
Disable-ServiceIfPresent @(
    "HvHost",
    "vmms",
    "vmicheartbeat",
    "vmickvpexchange",
    "vmicshutdown",
    "vmictimesync",
    "vmicvmsession",
    "vmicrdv",
    "SensorService",
    "SensorDataService",
    "SensrSvc",
    "WbioSrvc",
    "XboxNetApiSvc",
    "XboxGipSvc",
    "XblAuthManager",
    "XblGameSave",
    "DiagTrack",
    "MixedRealityOpenXRSvc",
    "WalletService",
    "SEMgrSvc",
    "lmhosts",
    "SCPolicySvc",
    "RetailDemo",
    "TapiSrv",
    "BDESVC",
    "AxInstSV",
    "TabletInputService",
    "WSearch",
    "SysMain",
    "Fax",
    "MapsBroker"
)
'''.strip(),
        }

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

    def _install_memory_cleaner(self, action: ToolkitAction) -> ExecutionResult:
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
            message="Windows Memory Cleaner installation completed" if success else "Windows Memory Cleaner installation failed",
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
