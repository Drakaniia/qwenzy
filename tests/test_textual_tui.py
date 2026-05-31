#!/usr/bin/env python3
"""Tests for the Textual-based toolkit interface."""

import ast
import asyncio
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)


def test_requirements_include_textual_8():
    """Textual should be declared as an application dependency."""
    requirements_path = os.path.join(ROOT_DIR, "requirements.txt")

    with open(requirements_path, "r", encoding="utf-8") as requirements_file:
        content = requirements_file.read()

    assert "textual>=8.2.7,<9.0.0" in content


def test_textual_stylesheet_exists_with_core_regions():
    """The Textual UI should keep styling in a dedicated TCSS file."""
    stylesheet_path = os.path.join(ROOT_DIR, "src", "tui", "toolkit.tcss")

    assert os.path.exists(stylesheet_path), "src/tui/toolkit.tcss is missing"

    with open(stylesheet_path, "r", encoding="utf-8") as stylesheet_file:
        content = stylesheet_file.read()

    for selector in ("#hero", "#workspace", "#activity-log", "DataTable:focus"):
        assert selector in content, f"stylesheet missing selector: {selector}"


def test_action_catalog_groups_existing_toolkit_features():
    """The TUI service should expose optimization-first toolkit actions."""
    from src.tui.services import ToolkitActionService

    service = ToolkitActionService(probe_tools=False)
    sections = service.get_sections()
    section_ids = {section.id for section in sections}

    assert {
        "debloat",
        "optimization",
        "settings",
        "power",
        "automation",
    }.issubset(section_ids)
    assert "apps" not in section_ids
    assert "ai" not in section_ids

    all_actions = [action for section in sections for action in section.actions]
    action_ids = {action.id for action in all_actions}
    action_types = {action.action_type for action in all_actions}

    assert "settings.performance" in action_ids
    assert "optimization.full" in action_ids
    assert "optimization.cleanup" in action_ids
    assert "optimization.privacy" in action_ids
    assert "optimization.services" in action_ids
    assert "power.active" in action_ids
    assert "automation.status" in action_ids
    assert "install_app" not in action_types
    assert "install_ai_tool" not in action_types

    assert any(action.requires_confirmation for action in all_actions)


def test_optimization_script_automates_optimize_md_settings():
    """The automated optimization payload should cover the documented tweak groups."""
    from src.tui.services import ToolkitActionService

    service = ToolkitActionService(probe_tools=False)
    full_action = service.find_action("optimization.full")
    script = service.build_optimization_script(full_action)

    expected_fragments = [
        "Checkpoint-Computer",
        "SoftwareDistribution\\Download",
        "netsh int tcp set global autotuninglevel=disabled",
        "congestionprovider=ctcp",
        "NonBestEffortLimit",
        "AllowGameDVR",
        "GameMode",
        "DisableTailoredExperiencesWithDiagnosticData",
        "DisableWindowsConsumerFeatures",
        "NoInstrumentation",
        "LaunchTo",
        "MouseSpeed",
        "StickyKeys",
        "DiagTrack",
        "SysMain",
        "XblGameSave",
        "TabletInputService",
    ]

    for fragment in expected_fragments:
        assert fragment in script, f"optimization script missing: {fragment}"


def test_windows_optimization_requires_admin_before_spawning_powershell(monkeypatch):
    """Admin-only optimization actions should fail before partial PowerShell execution."""
    from src.tui.services import ToolkitActionService

    class StandardUserSystem:
        is_admin = False
        documents_folder = os.path.join(ROOT_DIR, "Documents")

        def check_program_exists(self, _executable):
            return False

        def get_system_path(self, _path_key):
            return ""

    service = ToolkitActionService(StandardUserSystem(), probe_tools=False)
    network_action = service.find_action("optimization.network")
    subprocess_called = False

    def record_subprocess_call(*_args, **_kwargs):
        nonlocal subprocess_called
        subprocess_called = True
        return True, ""

    monkeypatch.setattr(service, "_run_subprocess", record_subprocess_call)

    result = service.run_action(network_action.id)

    assert not subprocess_called
    assert not result.success
    assert "Administrator" in result.message
    assert "HKLM" in result.details
    assert "netsh" in result.details


def test_confirmed_action_runs_from_normal_tui_action_path():
    """Confirmed actions should not require Textual worker context to open the modal."""
    from src.tui.app import ConfirmActionScreen, WindowsToolkitApp
    from src.tui.services import ExecutionResult, ToolkitAction, ToolkitSection

    class RecordingActionService:
        def __init__(self):
            self.action = ToolkitAction(
                id="optimization.full",
                section="optimization",
                title="Run Full Windows Optimization",
                target="Windows 10/11 automated optimization",
                description="Apply the complete automated optimization set.",
                action_type="windows_optimization",
                risk="High",
                requires_confirmation=True,
            )
            self.run_ids = []

        def get_sections(self):
            return [
                ToolkitSection(
                    id="optimization",
                    title="Optimization",
                    description="Apply Windows settings automatically.",
                    actions=[self.action],
                )
            ]

        def filter_actions(self, _query):
            return self.get_sections()

        def get_overview(self):
            return [
                ("Admin", "Ready", "Elevated session detected"),
                ("Winget", "Available", "Required for package-managed toolkit actions"),
                ("AutoHotKey", "Installed", "Automation script runtime"),
            ]

        def find_action(self, action_id):
            assert action_id == self.action.id
            return self.action

        def run_action(self, action_id):
            self.run_ids.append(action_id)
            return ExecutionResult(
                action_id=action_id,
                title=self.action.title,
                success=True,
                message="Optimization completed",
            )

    async def run_scenario():
        service = RecordingActionService()
        app = WindowsToolkitApp(service)

        async with app.run_test() as pilot:
            await app.action_run_selected()
            await pilot.pause()

            assert isinstance(app.screen, ConfirmActionScreen)
            assert service.run_ids == []

            await pilot.click("#confirm-run")
            await pilot.pause()

            assert service.run_ids == ["optimization.full"]

    asyncio.run(run_scenario())


def test_every_catalog_action_has_registered_executor(monkeypatch):
    """Every action exposed in every tab should dispatch to a service executor."""
    from src.tui.services import ExecutionResult, ToolkitActionService

    service = ToolkitActionService(probe_tools=False)
    actions = [action for section in service.get_sections() for action in section.actions]
    executed_action_ids = []

    known_action_types = {
        "automation_status",
        "create_autohotkey_startup",
        "install_autohotkey",
        "memory_cleaner",
        "open_power_options",
        "open_setting",
        "power_active",
        "power_list",
        "power_unlock",
        "powershell_url",
        "windows_optimization",
    }
    assert {action.action_type for action in actions} == known_action_types

    def record_result(action):
        executed_action_ids.append(action.id)
        return ExecutionResult(
            action_id=action.id,
            title=action.title,
            success=True,
            message=f"{action.title} dispatched",
        )

    monkeypatch.setattr(service, "_automation_status_result", record_result)
    monkeypatch.setattr(service, "_create_autohotkey_startup", record_result)
    monkeypatch.setattr(service, "_install_autohotkey", record_result)
    monkeypatch.setattr(service, "_install_memory_cleaner", record_result)
    monkeypatch.setattr(service, "_open_setting", record_result)
    monkeypatch.setattr(service, "_run_powershell_url", record_result)
    monkeypatch.setattr(service, "_run_windows_optimization", record_result)
    monkeypatch.setattr(service, "_unlock_ultimate_performance", record_result)
    monkeypatch.setattr(service, "_run_powercfg", lambda action, _command: record_result(action))

    for action in actions:
        result = service.run_action(action.id)
        assert result.success, result.message

    assert executed_action_ids == [action.id for action in actions]


def test_tui_can_run_every_catalog_action_from_every_tab():
    """The TUI run path should work for every row in every tab."""
    from textual.widgets import DataTable

    from src.tui.app import ConfirmActionScreen, WindowsToolkitApp
    from src.tui.services import ExecutionResult, ToolkitActionService

    sections = ToolkitActionService(probe_tools=False).get_sections()
    actions_by_id = {
        action.id: action
        for section in sections
        for action in section.actions
    }

    class RecordingActionService:
        def __init__(self):
            self.run_ids = []

        def get_sections(self):
            return sections

        def filter_actions(self, _query):
            return sections

        def get_overview(self):
            return [
                ("Admin", "Ready", "Elevated session detected"),
                ("Winget", "Available", "Required for package-managed toolkit actions"),
                ("AutoHotKey", "Installed", "Automation script runtime"),
            ]

        def find_action(self, action_id):
            return actions_by_id[action_id]

        def run_action(self, action_id):
            action = actions_by_id[action_id]
            self.run_ids.append(action_id)
            return ExecutionResult(
                action_id=action.id,
                title=action.title,
                success=True,
                message=f"{action.title} completed",
            )

    async def run_scenario():
        service = RecordingActionService()
        app = WindowsToolkitApp(service)

        async with app.run_test(size=(120, 40)) as pilot:
            expected_run_ids = []

            for section in sections:
                table = app.query_one(f"#table-{section.id}", DataTable)
                assert table.row_count == len(section.actions)

                for action in section.actions:
                    app.active_section_id = section.id
                    app.selected_action_id = action.id
                    expected_run_ids.append(action.id)

                    await app.action_run_selected()
                    await pilot.pause()

                    if action.requires_confirmation:
                        assert isinstance(app.screen, ConfirmActionScreen)
                        await pilot.click("#confirm-run")

                    for _ in range(10):
                        if service.run_ids == expected_run_ids:
                            break
                        await pilot.pause(0.01)

                    assert service.run_ids == expected_run_ids

    asyncio.run(run_scenario())


def test_status_overview_removes_ai_tool_dependency_card():
    """The status sidebar should no longer advertise Node/npm for AI tool installs."""
    from src.tui.services import ToolkitActionService

    service = ToolkitActionService(probe_tools=False)
    labels = [label for label, _value, _detail in service.get_overview()]

    assert "Node/npm" not in labels
    assert labels == ["Admin", "Winget", "AutoHotKey"]


def test_app_and_ai_installer_modules_are_removed():
    """The removed installer features should not remain as importable modules."""
    removed_modules = [
        os.path.join(ROOT_DIR, "src", "modules", "installer.py"),
        os.path.join(ROOT_DIR, "src", "modules", "ai_tools.py"),
    ]

    for module_path in removed_modules:
        assert not os.path.exists(module_path), f"removed installer module still exists: {module_path}"


def test_main_is_textual_only_without_legacy_cli():
    """The main entrypoint should expose only the Textual app."""
    main_path = os.path.join(ROOT_DIR, "main.py")

    with open(main_path, "r", encoding="utf-8") as main_file:
        source = main_file.read()
        tree = ast.parse(source)

    imported_names = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.ImportFrom) and node.module == "src.tui.app"
        for alias in node.names
    }

    assert "WindowsToolkitApp" in imported_names

    assert "WindowsToolkitApp().run()" in source
    assert "--legacy-cli" not in source
    assert "WindowsAutomationToolkit" not in source
    assert "show_debloat_menu" not in source
    assert "src.modules." not in source
