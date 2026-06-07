#!/usr/bin/env python3
"""Tests for PowerShell launcher scripts."""

import os
import re


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_script(name):
    path = os.path.join(ROOT_DIR, "scripts", name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_install_launcher_uses_published_executable_name():
    content = read_script("install.ps1")

    assert 'WindowsToolkit.exe' in content
    assert 'WindowsAutomationToolkit.exe' not in content


def test_install_launcher_requests_elevation_for_toolkit():
    content = read_script("install.ps1")

    assert re.search(r"Start-Process\s+-FilePath\s+\$ExePath\s+-Verb\s+RunAs", content)


def test_run_exe_launcher_uses_published_executable_name():
    content = read_script("run-exe.ps1")

    assert 'WindowsToolkit.exe' in content
    assert 'WindowsAutomationToolkit.exe' not in content


def test_run_exe_launcher_requests_elevation_for_toolkit():
    content = read_script("run-exe.ps1")

    assert re.search(r"Start-Process\s+-FilePath\s+\$ExePath\s+-Verb\s+RunAs", content)
