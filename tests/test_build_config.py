#!/usr/bin/env python3
"""Tests for PyInstaller build configuration"""

import os
import sys
import subprocess
import ast

# Add root directory to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)


def test_requirements_contains_pyinstaller():
    """Test that requirements.txt contains pyinstaller>=6.0.0"""
    requirements_path = os.path.join(ROOT_DIR, 'requirements.txt')
    
    assert os.path.exists(requirements_path), f"requirements.txt not found at {requirements_path}"
    
    with open(requirements_path, 'r') as f:
        content = f.read()
    
    assert 'pyinstaller' in content.lower(), "requirements.txt does not contain 'pyinstaller'"
    assert 'pyinstaller>=6.0.0' in content, "requirements.txt does not contain 'pyinstaller>=6.0.0'"
    print("✓ requirements.txt contains pyinstaller>=6.0.0")


def test_toolkit_spec_exists():
    """Test that build/toolkit.spec exists"""
    spec_path = os.path.join(ROOT_DIR, 'build', 'toolkit.spec')
    
    assert os.path.exists(spec_path), f"toolkit.spec not found at {spec_path}"
    print("✓ build/toolkit.spec exists")


def test_toolkit_spec_has_required_structure():
    """Test that toolkit.spec has required PyInstaller structure"""
    spec_path = os.path.join(ROOT_DIR, 'build', 'toolkit.spec')
    
    with open(spec_path, 'r') as f:
        content = f.read()
    
    # Check for required PyInstaller components
    required_elements = [
        'Analysis(',
        'PYZ(',
        'EXE(',
        "'../main.py'",
        "name='WindowsAutomationToolkit'",
        'datas=',
        'hiddenimports=',
    ]
    
    for element in required_elements:
        assert element in content, f"toolkit.spec missing required element: {element}"
    
    print("✓ build/toolkit.spec has required structure")


def test_toolkit_spec_includes_source_modules():
    """Test that toolkit.spec includes all source modules"""
    spec_path = os.path.join(ROOT_DIR, 'build', 'toolkit.spec')
    
    with open(spec_path, 'r') as f:
        content = f.read()
    
    # Check for required module imports
    required_modules = [
        'src.config.settings',
        'src.utils.system',
        'src.modules.debloat',
        'src.modules.settings',
        'src.modules.power',
        'src.modules.installer',
        'src.modules.ai_tools',
        'src.modules.autohotkey',
    ]
    
    for module in required_modules:
        assert module in content, f"toolkit.spec missing hiddenimport: {module}"
    
    print("✓ build/toolkit.spec includes all source modules")


def test_build_executable_script_exists():
    """Test that build/build-executable.py exists"""
    script_path = os.path.join(ROOT_DIR, 'build', 'build-executable.py')
    
    assert os.path.exists(script_path), f"build-executable.py not found at {script_path}"
    print("✓ build/build-executable.py exists")


def test_build_executable_script_valid_syntax():
    """Test that build-executable.py has valid Python syntax"""
    script_path = os.path.join(ROOT_DIR, 'build', 'build-executable.py')
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # This will raise SyntaxError if syntax is invalid
    ast.parse(content)
    print("✓ build/build-executable.py has valid Python syntax")


def test_build_executable_script_has_build_function():
    """Test that build-executable.py contains build_executable function"""
    script_path = os.path.join(ROOT_DIR, 'build', 'build-executable.py')
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    assert 'def build_executable():' in content, "build-executable.py missing build_executable() function"
    assert "if __name__ == '__main__':" in content, "build-executable.py missing main guard"
    print("✓ build/build-executable.py has build_executable function")


def test_build_executable_script_references_spec():
    """Test that build-executable.py references toolkit.spec"""
    script_path = os.path.join(ROOT_DIR, 'build', 'build-executable.py')
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    assert 'toolkit.spec' in content, "build-executable.py does not reference toolkit.spec"
    assert 'PyInstaller' in content, "build-executable.py does not reference PyInstaller"
    print("✓ build/build-executable.py references toolkit.spec")


def test_launcher_directory_in_gitignore():
    """Test that launcher/ directory is in .gitignore"""
    gitignore_path = os.path.join(ROOT_DIR, '.gitignore')
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    assert 'launcher/' in content, ".gitignore does not contain 'launcher/'"
    print("✓ launcher/ directory is in .gitignore")


if __name__ == '__main__':
    # Run all tests
    tests = [
        test_requirements_contains_pyinstaller,
        test_toolkit_spec_exists,
        test_toolkit_spec_has_required_structure,
        test_toolkit_spec_includes_source_modules,
        test_build_executable_script_exists,
        test_build_executable_script_valid_syntax,
        test_build_executable_script_has_build_function,
        test_build_executable_script_references_spec,
        test_launcher_directory_in_gitignore,
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
