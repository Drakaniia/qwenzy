"""Business-facing service layer for the Textual interface."""

from __future__ import annotations

from src.modules.autohotkey import AutoHotKeyManager
from src.modules.power import PowerManagement
from src.modules.windows_settings import WindowsSettings
from src.tui.executor import ToolkitActionExecutorMixin
from src.tui.models import ExecutionResult, ToolkitAction, ToolkitSection
from src.tui.script_builder import build_optimization_script as _build_optimization_script
from src.tui.sections import ToolkitSectionBuilderMixin
from src.utils.system import SystemUtils

__all__ = [
    "ExecutionResult",
    "ToolkitAction",
    "ToolkitActionService",
    "ToolkitSection",
]


class ToolkitActionService(ToolkitSectionBuilderMixin, ToolkitActionExecutorMixin):
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

    def build_optimization_script(self, action: ToolkitAction) -> str:
        """Build the PowerShell script for a Windows optimization action."""
        return _build_optimization_script(action.payload.get("groups", []))
