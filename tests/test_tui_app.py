#!/usr/bin/env python3
"""Tests for the Textual application layer (app wiring, screens, entry point)."""

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
