#!/usr/bin/env python3
"""Tests for Inno Setup installer configuration"""

import os
import sys
import subprocess
import ast

# Add root directory to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)


def test_inno_setup_script_exists():
    """Test that build/create-installer.iss exists"""
    iss_path = os.path.join(ROOT_DIR, 'build', 'create-installer.iss')

    assert os.path.exists(iss_path), f"create-installer.iss not found at {iss_path}"
    print("✓ build/create-installer.iss exists")


def test_inno_setup_script_has_required_sections():
    """Test that create-installer.iss has required Inno Setup sections"""
    iss_path = os.path.join(ROOT_DIR, 'build', 'create-installer.iss')

    with open(iss_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required Inno Setup sections
    required_sections = [
        '[Setup]',
        '[Files]',
        '[Icons]',
        '[Run]',
    ]

    for section in required_sections:
        assert section in content, f"create-installer.iss missing required section: {section}"

    print("✓ build/create-installer.iss has required sections")


def test_inno_setup_script_has_app_definitions():
    """Test that create-installer.iss has application definitions"""
    iss_path = os.path.join(ROOT_DIR, 'build', 'create-installer.iss')

    with open(iss_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required app definitions
    required_definitions = [
        '#define MyAppName',
        '#define MyAppVersion',
        '#define MyAppExeName',
    ]

    for definition in required_definitions:
        assert definition in content, f"create-installer.iss missing definition: {definition}"

    print("✓ build/create-installer.iss has application definitions")


def test_inno_setup_script_has_setup_directives():
    """Test that create-installer.iss has required Setup directives"""
    iss_path = os.path.join(ROOT_DIR, 'build', 'create-installer.iss')

    with open(iss_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required Setup directives
    required_directives = [
        'AppId=',
        'AppName={#MyAppName}',
        'AppVersion={#MyAppVersion}',
        'DefaultDirName=',
        'OutputDir=',
        'OutputBaseFilename=',
        'Compression=',
    ]

    for directive in required_directives:
        assert directive in content, f"create-installer.iss missing directive: {directive}"

    print("✓ build/create-installer.iss has required Setup directives")


def test_inno_setup_script_references_launcher_executable():
    """Test that create-installer.iss references the launcher executable"""
    iss_path = os.path.join(ROOT_DIR, 'build', 'create-installer.iss')

    with open(iss_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'WindowsAutomationToolkit.exe' in content, \
        "create-installer.iss does not reference WindowsAutomationToolkit.exe"
    assert '..\\launcher\\' in content or '../launcher/' in content, \
        "create-installer.iss does not reference launcher directory"

    print("✓ build/create-installer.iss references launcher executable")


def test_inno_setup_script_has_windows_version_check():
    """Test that create-installer.iss has Windows version check in [Code] section"""
    iss_path = os.path.join(ROOT_DIR, 'build', 'create-installer.iss')

    with open(iss_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '[Code]' in content, "create-installer.iss missing [Code] section"
    assert 'GetWindowsVersion' in content, \
        "create-installer.iss missing Windows version check"
    assert 'Windows 10' in content, \
        "create-installer.iss missing Windows 10 requirement message"

    print("✓ build/create-installer.iss has Windows version check")


def test_inno_setup_script_has_languages_section():
    """Test that create-installer.iss has [Languages] section"""
    iss_path = os.path.join(ROOT_DIR, 'build', 'create-installer.iss')

    with open(iss_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '[Languages]' in content, "create-installer.iss missing [Languages] section"
    assert 'english' in content.lower(), "create-installer.iss missing English language"

    print("✓ build/create-installer.iss has Languages section")


def test_inno_setup_script_has_tasks_section():
    """Test that create-installer.iss has [Tasks] section with desktop and startup icons"""
    iss_path = os.path.join(ROOT_DIR, 'build', 'create-installer.iss')

    with open(iss_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '[Tasks]' in content, "create-installer.iss missing [Tasks] section"
    assert 'desktopicon' in content.lower(), \
        "create-installer.iss missing desktop icon task"
    assert 'startupicon' in content.lower() or 'autostartup' in content.lower(), \
        "create-installer.iss missing startup icon task"

    print("✓ build/create-installer.iss has Tasks section")


def test_build_installer_batch_exists():
    """Test that build/build-installer.bat exists"""
    bat_path = os.path.join(ROOT_DIR, 'build', 'build-installer.bat')

    assert os.path.exists(bat_path), f"build-installer.bat not found at {bat_path}"
    print("✓ build/build-installer.bat exists")


def test_build_installer_batch_valid_syntax():
    """Test that build-installer.bat has valid batch syntax"""
    bat_path = os.path.join(ROOT_DIR, 'build', 'build-installer.bat')

    with open(bat_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for essential batch file elements
    assert '@echo off' in content, "build-installer.bat missing '@echo off'"
    assert 'ISCC' in content, "build-installer.bat missing ISCC variable"
    assert 'create-installer.iss' in content, \
        "build-installer.bat does not reference create-installer.iss"

    print("✓ build/build-installer.bat has valid batch structure")


def test_build_installer_batch_checks_inno_setup():
    """Test that build-installer.bat checks for Inno Setup installation"""
    bat_path = os.path.join(ROOT_DIR, 'build', 'build-installer.bat')

    with open(bat_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'Program Files' in content or 'ProgramFiles' in content, \
        "build-installer.bat does not check Program Files for Inno Setup"
    assert 'if not exist' in content.lower(), \
        "build-installer.bat missing existence check for Inno Setup"

    print("✓ build/build-installer.bat checks for Inno Setup installation")


def test_build_installer_batch_handles_errors():
    """Test that build-installer.bat handles build errors"""
    bat_path = os.path.join(ROOT_DIR, 'build', 'build-installer.bat')

    with open(bat_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'ERRORLEVEL' in content, "build-installer.bat does not check ERRORLEVEL"
    assert 'exit /b' in content.lower(), \
        "build-installer.bat does not have error exit handling"

    print("✓ build/build-installer.bat handles build errors")


def test_installer_directory_in_gitignore():
    """Test that installer/ directory is in .gitignore"""
    gitignore_path = os.path.join(ROOT_DIR, '.gitignore')

    with open(gitignore_path, 'r') as f:
        content = f.read()

    assert 'installer/' in content, ".gitignore does not contain 'installer/'"
    print("✓ installer/ directory is in .gitignore")


def test_license_file_exists():
    """Test that LICENSE file exists (required by ISS script)"""
    license_path = os.path.join(ROOT_DIR, 'LICENSE')

    assert os.path.exists(license_path), \
        f"LICENSE file not found at {license_path}. Required by Inno Setup script."
    print("✓ LICENSE file exists")


if __name__ == '__main__':
    # Run all tests
    tests = [
        test_inno_setup_script_exists,
        test_inno_setup_script_has_required_sections,
        test_inno_setup_script_has_app_definitions,
        test_inno_setup_script_has_setup_directives,
        test_inno_setup_script_references_launcher_executable,
        test_inno_setup_script_has_windows_version_check,
        test_inno_setup_script_has_languages_section,
        test_inno_setup_script_has_tasks_section,
        test_build_installer_batch_exists,
        test_build_installer_batch_valid_syntax,
        test_build_installer_batch_checks_inno_setup,
        test_build_installer_batch_handles_errors,
        test_installer_directory_in_gitignore,
        test_license_file_exists,
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
