#!/usr/bin/env python3
"""Tests for installation documentation"""

import os
import sys

# Add root directory to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)


def test_installation_guide_exists():
    """Test that docs/INSTALLATION.md exists"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    assert os.path.exists(doc_path), f"INSTALLATION.md not found at {doc_path}"
    print("✓ docs/INSTALLATION.md exists")


def test_installation_guide_has_title():
    """Test that INSTALLATION.md has the correct title"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '# Installation Guide - Windows Automation Toolkit' in content, \
        "INSTALLATION.md missing correct title"
    print("✓ docs/INSTALLATION.md has correct title")


def test_installation_guide_has_choose_method_section():
    """Test that INSTALLATION.md has 'Choose Your Installation Method' section"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '## Choose Your Installation Method' in content, \
        "INSTALLATION.md missing 'Choose Your Installation Method' section"
    print("✓ docs/INSTALLATION.md has 'Choose Your Installation Method' section")


def test_installation_guide_has_powershell_method():
    """Test that INSTALLATION.md has PowerShell One-Liner method"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '### Method 1: PowerShell One-Liner' in content, \
        "INSTALLATION.md missing PowerShell One-Liner method"
    assert 'No Python required' in content, \
        "INSTALLATION.md missing 'No Python required' note for Method 1"
    assert 'powershell -ExecutionPolicy Bypass' in content, \
        "INSTALLATION.md missing PowerShell command"
    print("✓ docs/INSTALLATION.md has PowerShell One-Liner method")


def test_installation_guide_has_standalone_executable_method():
    """Test that INSTALLATION.md has Standalone Executable method"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '### Method 2: Standalone Executable' in content, \
        "INSTALLATION.md missing Standalone Executable method"
    assert 'Releases' in content, \
        "INSTALLATION.md missing Releases link for Method 2"
    assert 'WindowsAutomationToolkit.exe' in content, \
        "INSTALLATION.md missing executable name"
    print("✓ docs/INSTALLATION.md has Standalone Executable method")


def test_installation_guide_has_traditional_installer_method():
    """Test that INSTALLATION.md has Traditional Installer method"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '### Method 3: Traditional Installer' in content, \
        "INSTALLATION.md missing Traditional Installer method"
    assert 'WindowsAutomationToolkit-Setup.exe' in content, \
        "INSTALLATION.md missing installer name"
    assert 'Start Menu' in content, \
        "INSTALLATION.md missing Start Menu reference"
    assert 'Control Panel' in content, \
        "INSTALLATION.md missing Control Panel reference"
    print("✓ docs/INSTALLATION.md has Traditional Installer method")


def test_installation_guide_has_python_source_method():
    """Test that INSTALLATION.md has Python Source method"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '### Method 4: Python Source' in content, \
        "INSTALLATION.md missing Python Source method"
    assert 'Requires Python 3.10+' in content, \
        "INSTALLATION.md missing Python version requirement"
    assert 'git clone' in content, \
        "INSTALLATION.md missing git clone command"
    assert 'pip install -r requirements.txt' in content, \
        "INSTALLATION.md missing pip install command"
    print("✓ docs/INSTALLATION.md has Python Source method")


def test_installation_guide_has_pros_and_cons():
    """Test that INSTALLATION.md has pros and cons for each method"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '**Pros:**' in content, "INSTALLATION.md missing Pros sections"
    assert '**Cons:**' in content, "INSTALLATION.md missing Cons sections"
    assert '✅' in content, "INSTALLATION.md missing checkmark icons for pros"
    assert '❌' in content, "INSTALLATION.md missing cross icons for cons"
    print("✓ docs/INSTALLATION.md has pros and cons for each method")


def test_installation_guide_has_system_requirements():
    """Test that INSTALLATION.md has System Requirements section"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '## System Requirements' in content, \
        "INSTALLATION.md missing System Requirements section"
    assert 'Windows 10' in content, \
        "INSTALLATION.md missing Windows version requirement"
    assert 'RAM:' in content, \
        "INSTALLATION.md missing RAM requirement"
    assert 'Disk:' in content or 'Storage:' in content, \
        "INSTALLATION.md missing disk space requirement"
    assert 'Administrator' in content, \
        "INSTALLATION.md missing administrator privilege requirement"
    print("✓ docs/INSTALLATION.md has System Requirements section")


def test_installation_guide_has_troubleshooting():
    """Test that INSTALLATION.md has Troubleshooting section"""
    doc_path = os.path.join(ROOT_DIR, 'docs', 'INSTALLATION.md')

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '## Troubleshooting' in content, \
        "INSTALLATION.md missing Troubleshooting section"
    assert 'PowerShell scripts' in content, \
        "INSTALLATION.md missing PowerShell troubleshooting"
    assert 'SmartScreen' in content, \
        "INSTALLATION.md missing SmartScreen troubleshooting"
    assert 'python.org' in content, \
        "INSTALLATION.md missing Python installation troubleshooting"
    assert 'winget' in content, \
        "INSTALLATION.md missing winget troubleshooting"
    print("✓ docs/INSTALLATION.md has Troubleshooting section")


def test_readme_has_installation_options():
    """Test that Readme.md has Installation Options section"""
    readme_path = os.path.join(ROOT_DIR, 'Readme.md')

    assert os.path.exists(readme_path), f"Readme.md not found at {readme_path}"

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '## Installation Options' in content, \
        "Readme.md missing Installation Options section"
    print("✓ Readme.md has Installation Options section")


def test_readme_has_quick_install_command():
    """Test that Readme.md has Quick Install PowerShell command"""
    readme_path = os.path.join(ROOT_DIR, 'Readme.md')

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'powershell -ExecutionPolicy Bypass' in content, \
        "Readme.md missing Quick Install PowerShell command"
    assert 'iwr' in content, \
        "Readme.md missing iwr (Invoke-WebRequest) command"
    assert 'iex' in content, \
        "Readme.md missing iex (Invoke-Expression) command"
    print("✓ Readme.md has Quick Install PowerShell command")


def test_readme_has_releases_link():
    """Test that Readme.md has Releases link"""
    readme_path = os.path.join(ROOT_DIR, 'Readme.md')

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'Releases' in content, \
        "Readme.md missing Releases reference"
    assert 'github.com' in content, \
        "Readme.md missing GitHub URL"
    assert 'windows-automation-toolkit/releases' in content, \
        "Readme.md missing releases path"
    print("✓ Readme.md has Releases link")


def test_readme_links_to_installation_guide():
    """Test that Readme.md links to docs/INSTALLATION.md"""
    readme_path = os.path.join(ROOT_DIR, 'Readme.md')

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'docs/INSTALLATION.md' in content, \
        "Readme.md missing link to docs/INSTALLATION.md"
    assert 'Full Installation Guide' in content, \
        "Readme.md missing Full Installation Guide reference"
    print("✓ Readme.md links to docs/INSTALLATION.md")


def test_readme_mentions_no_python_required():
    """Test that Readme.md mentions 'No Python Required' option"""
    readme_path = os.path.join(ROOT_DIR, 'Readme.md')

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'No Python' in content or 'no Python' in content, \
        "Readme.md missing 'No Python Required' mention"
    print("✓ Readme.md mentions 'No Python Required' option")


if __name__ == '__main__':
    # Run all tests
    tests = [
        test_installation_guide_exists,
        test_installation_guide_has_title,
        test_installation_guide_has_choose_method_section,
        test_installation_guide_has_powershell_method,
        test_installation_guide_has_standalone_executable_method,
        test_installation_guide_has_traditional_installer_method,
        test_installation_guide_has_python_source_method,
        test_installation_guide_has_pros_and_cons,
        test_installation_guide_has_system_requirements,
        test_installation_guide_has_troubleshooting,
        test_readme_has_installation_options,
        test_readme_has_quick_install_command,
        test_readme_has_releases_link,
        test_readme_links_to_installation_guide,
        test_readme_mentions_no_python_required,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Tests: {passed + failed} | Passed: {passed} | Failed: {failed}")

    if failed > 0:
        sys.exit(1)
