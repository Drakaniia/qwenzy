#!/usr/bin/env python3
"""Tests for the Textual-based toolkit interface."""

import ast
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
