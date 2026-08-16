#!/usr/bin/env python3
"""Tests for the Textual toolkit service layer (catalog, scripts, executors)."""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)


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


def test_optimization_apps_include_bleachbit_and_memreduct():
    """The installable optimization apps should cover BleachBit and MemReduct with choco/winget methods."""
    from src.tui.services import ToolkitActionService

    service = ToolkitActionService(probe_tools=False)
    actions_by_id = {
        action.id: action
        for section in service.get_sections()
        for action in section.actions
    }

    bleachbit = actions_by_id["debloat.optimization_apps.bleachbit"]
    assert bleachbit.title == "BleachBit"
    assert bleachbit.payload["script"]["install_methods"] == {
        "choco": "choco install bleachbit",
        "winget": "winget install BleachBit.BleachBit",
    }

    memreduct = actions_by_id["debloat.optimization_apps.memreduct"]
    assert memreduct.title == "MemReduct"
    assert memreduct.payload["script"]["install_methods"] == {
        "choco": "choco install memreduct",
        "winget": "winget install Henry++.MemReduct",
    }


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
        "install_optimization_app",
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
    monkeypatch.setattr(service, "_install_optimization_app", record_result)
    monkeypatch.setattr(service, "_open_setting", record_result)
    monkeypatch.setattr(service, "_run_powershell_url", record_result)
    monkeypatch.setattr(service, "_run_windows_optimization", record_result)
    monkeypatch.setattr(service, "_unlock_ultimate_performance", record_result)
    monkeypatch.setattr(service, "_run_powercfg", lambda action, _command: record_result(action))

    for action in actions:
        result = service.run_action(action.id)
        assert result.success, result.message

    assert executed_action_ids == [action.id for action in actions]


def test_status_overview_removes_ai_tool_dependency_card():
    """The status sidebar should no longer advertise Node/npm for AI tool installs."""
    from src.tui.services import ToolkitActionService

    service = ToolkitActionService(probe_tools=False)
    labels = [label for label, _value, _detail in service.get_overview()]

    assert "Node/npm" not in labels
    assert labels == ["Admin", "Winget", "AutoHotKey"]
