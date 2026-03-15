#!/usr/bin/env python3
"""Tests for GitHub Actions workflow configuration"""

import os
import sys
import yaml

# Add root directory to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)


def test_workflows_directory_exists():
    """Test that .github/workflows directory exists"""
    workflows_dir = os.path.join(ROOT_DIR, '.github', 'workflows')

    assert os.path.isdir(workflows_dir), f".github/workflows directory not found at {workflows_dir}"
    print("✓ .github/workflows directory exists")


def test_release_workflow_exists():
    """Test that release.yml workflow exists"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    assert os.path.exists(workflow_path), f"release.yml not found at {workflow_path}"
    print("✓ .github/workflows/release.yml exists")


def test_build_executable_workflow_exists():
    """Test that build-executable.yml workflow exists"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'build-executable.yml')

    assert os.path.exists(workflow_path), f"build-executable.yml not found at {workflow_path}"
    print("✓ .github/workflows/build-executable.yml exists")


def test_release_workflow_valid_yaml():
    """Test that release.yml has valid YAML syntax"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    # This will raise yaml.YAMLError if syntax is invalid
    yaml.safe_load(content)
    print("✓ release.yml has valid YAML syntax")


def test_build_executable_workflow_valid_yaml():
    """Test that build-executable.yml has valid YAML syntax"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'build-executable.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    # This will raise yaml.YAMLError if syntax is invalid
    yaml.safe_load(content)
    print("✓ build-executable.yml has valid YAML syntax")


def test_release_workflow_has_correct_trigger():
    """Test that release.yml triggers on version tags"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    assert 'on' in workflow or True in workflow, "release.yml missing 'on' trigger section"
    
    # Handle both 'on' and True (yaml parses 'on' as True in some versions)
    trigger_section = workflow.get('on') or workflow.get(True)
    assert trigger_section is not None, "release.yml missing trigger configuration"
    
    assert 'push' in trigger_section, "release.yml missing 'push' trigger"
    assert 'tags' in trigger_section['push'], "release.yml missing 'tags' in push trigger"
    assert "'v*'" in str(trigger_section['push']['tags']) or 'v*' in str(trigger_section['push']['tags']), \
        "release.yml missing 'v*' tag pattern"
    
    print("✓ release.yml has correct trigger (push on v* tags)")


def test_release_workflow_has_build_executable_job():
    """Test that release.yml has build-executable job"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    jobs = workflow.get('jobs', {})
    assert 'build-executable' in jobs, "release.yml missing 'build-executable' job"
    
    job = jobs['build-executable']
    assert 'runs-on' in job, "build-executable job missing 'runs-on'"
    assert job['runs-on'] == 'windows-latest', "build-executable job should run on windows-latest"
    
    print("✓ release.yml has build-executable job")


def test_release_workflow_has_build_installer_job():
    """Test that release.yml has build-installer job"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    jobs = workflow.get('jobs', {})
    assert 'build-installer' in jobs, "release.yml missing 'build-installer' job"
    
    job = jobs['build-installer']
    assert 'runs-on' in job, "build-installer job missing 'runs-on'"
    assert job['runs-on'] == 'windows-latest', "build-installer job should run on windows-latest"
    assert 'needs' in job, "build-installer job missing 'needs' dependency"
    assert 'build-executable' in job['needs'], "build-installer should need build-executable"
    
    print("✓ release.yml has build-installer job with correct dependency")


def test_release_workflow_has_create_release_job():
    """Test that release.yml has create-release job"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    jobs = workflow.get('jobs', {})
    assert 'create-release' in jobs, "release.yml missing 'create-release' job"
    
    job = jobs['create-release']
    assert 'runs-on' in job, "create-release job missing 'runs-on'"
    assert job['runs-on'] == 'windows-latest', "create-release job should run on windows-latest"
    assert 'needs' in job, "create-release job missing 'needs' dependency"
    assert 'build-executable' in job['needs'] and 'build-installer' in job['needs'], \
        "create-release should need both build-executable and build-installer"
    
    print("✓ release.yml has create-release job with correct dependencies")


def test_release_workflow_uses_correct_actions():
    """Test that release.yml uses required GitHub Actions"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    required_actions = [
        'actions/checkout@v4',
        'actions/setup-python@v5',
        'actions/upload-artifact@v4',
        'actions/download-artifact@v4',
        'softprops/action-gh-release@v1',
    ]

    for action in required_actions:
        assert action in content, f"release.yml missing required action: {action}"

    print("✓ release.yml uses all required GitHub Actions")


def test_release_workflow_builds_executable_correctly():
    """Test that release.yml builds executable with correct script"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    assert 'python build/build-executable.py' in content, \
        "release.yml missing 'python build/build-executable.py' command"
    assert 'WindowsAutomationToolkit.exe' in content, \
        "release.yml missing reference to WindowsAutomationToolkit.exe"
    
    print("✓ release.yml builds executable correctly")


def test_release_workflow_builds_installer_correctly():
    """Test that release.yml builds installer with correct script"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    assert 'build-installer.bat' in content or 'build-installer.cmd' in content, \
        "release.yml missing reference to build-installer.bat"
    assert 'WindowsAutomationToolkit-Setup.exe' in content, \
        "release.yml missing reference to WindowsAutomationToolkit-Setup.exe"
    
    print("✓ release.yml builds installer correctly")


def test_release_workflow_has_release_files():
    """Test that release.yml includes correct files in release"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    assert 'WindowsAutomationToolkit.exe' in content, \
        "release.yml missing WindowsAutomationToolkit.exe in release files"
    assert 'WindowsAutomationToolkit-Setup.exe' in content, \
        "release.yml missing WindowsAutomationToolkit-Setup.exe in release files"
    
    print("✓ release.yml includes correct files in release")


def test_build_executable_workflow_has_correct_trigger():
    """Test that build-executable.yml triggers on pull requests"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'build-executable.yml')

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    assert 'on' in workflow or True in workflow, "build-executable.yml missing 'on' trigger section"
    
    # Handle both 'on' and True (yaml parses 'on' as True in some versions)
    trigger_section = workflow.get('on') or workflow.get(True)
    assert trigger_section is not None, "build-executable.yml missing trigger configuration"
    
    assert 'pull_request' in trigger_section, "build-executable.yml missing 'pull_request' trigger"
    assert 'branches' in trigger_section['pull_request'], \
        "build-executable.yml missing 'branches' in pull_request trigger"
    
    print("✓ build-executable.yml has correct trigger (pull_request on main)")


def test_build_executable_workflow_has_build_job():
    """Test that build-executable.yml has build job"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'build-executable.yml')

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    jobs = workflow.get('jobs', {})
    assert 'build' in jobs, "build-executable.yml missing 'build' job"
    
    job = jobs['build']
    assert 'runs-on' in job, "build job missing 'runs-on'"
    assert job['runs-on'] == 'windows-latest', "build job should run on windows-latest"
    
    print("✓ build-executable.yml has build job")


def test_build_executable_workflow_uses_correct_actions():
    """Test that build-executable.yml uses required GitHub Actions"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'build-executable.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    required_actions = [
        'actions/checkout@v4',
        'actions/setup-python@v5',
    ]

    for action in required_actions:
        assert action in content, f"build-executable.yml missing required action: {action}"

    print("✓ build-executable.yml uses all required GitHub Actions")


def test_build_executable_workflow_builds_correctly():
    """Test that build-executable.yml builds executable with correct script"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'build-executable.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    assert 'python build/build-executable.py' in content, \
        "build-executable.yml missing 'python build/build-executable.py' command"
    assert 'WindowsAutomationToolkit.exe' in content, \
        "build-executable.yml missing reference to WindowsAutomationToolkit.exe"
    
    print("✓ build-executable.yml builds executable correctly")


def test_build_executable_workflow_has_test_step():
    """Test that build-executable.yml has test step for executable"""
    workflow_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'build-executable.yml')

    with open(workflow_path, 'r') as f:
        content = f.read()

    assert 'Test-Path' in content, "build-executable.yml missing Test-Path command"
    assert 'WindowsAutomationToolkit.exe' in content, \
        "build-executable.yml missing executable path check"
    
    print("✓ build-executable.yml has test step for executable")


def test_workflows_use_python_3_11():
    """Test that both workflows use Python 3.11"""
    release_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'release.yml')
    build_path = os.path.join(ROOT_DIR, '.github', 'workflows', 'build-executable.yml')

    for workflow_path, workflow_name in [(release_path, 'release.yml'), (build_path, 'build-executable.yml')]:
        with open(workflow_path, 'r') as f:
            content = f.read()

        assert "python-version: '3.11'" in content or 'python-version: "3.11"' in content, \
            f"{workflow_name} should use Python 3.11"

    print("✓ Both workflows use Python 3.11")


if __name__ == '__main__':
    # Run all tests
    tests = [
        test_workflows_directory_exists,
        test_release_workflow_exists,
        test_build_executable_workflow_exists,
        test_release_workflow_valid_yaml,
        test_build_executable_workflow_valid_yaml,
        test_release_workflow_has_correct_trigger,
        test_release_workflow_has_build_executable_job,
        test_release_workflow_has_build_installer_job,
        test_release_workflow_has_create_release_job,
        test_release_workflow_uses_correct_actions,
        test_release_workflow_builds_executable_correctly,
        test_release_workflow_builds_installer_correctly,
        test_release_workflow_has_release_files,
        test_build_executable_workflow_has_correct_trigger,
        test_build_executable_workflow_has_build_job,
        test_build_executable_workflow_uses_correct_actions,
        test_build_executable_workflow_builds_correctly,
        test_build_executable_workflow_has_test_step,
        test_workflows_use_python_3_11,
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
