"""Action catalog section builders for the Textual interface."""

from __future__ import annotations

from src.config.settings import (
    POWERSHELL_SCRIPTS,
    ULTIMATE_PERFORMANCE_GUID,
    WINDOWS_COMMANDS,
    WINDOWS_OPTIMIZATION_ACTIONS,
)
from src.tui.models import ToolkitAction, ToolkitSection


class ToolkitSectionBuilderMixin:
    """Build the grouped action catalog shown in the TUI tabs."""

    def _debloat_section(self) -> ToolkitSection:
        actions: list[ToolkitAction] = []

        for category, scripts in POWERSHELL_SCRIPTS.items():
            for key, script in scripts.items():
                if category == "optimization_apps":
                    actions.append(
                        ToolkitAction(
                            id=f"debloat.{category}.{key}",
                            section="debloat",
                            title=script["name"],
                            target="winget or Chocolatey",
                            description=script["description"],
                            action_type="install_optimization_app",
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
            description="Run curated Windows cleanup, tweak, and activation scripts, and install optimization apps via winget or Chocolatey.",
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
