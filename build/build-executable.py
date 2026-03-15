#!/usr/bin/env python3
"""Build standalone executable using PyInstaller"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the standalone executable"""
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(root_dir, 'launcher')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean previous builds
    build_dir = os.path.join(script_dir, 'build')
    dist_dir = os.path.join(script_dir, 'dist')
    
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    # Run PyInstaller
    spec_file = os.path.join(script_dir, 'toolkit.spec')
    
    print("Building executable with PyInstaller...")
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--distpath', output_dir,
        '--workpath', build_dir,
        '--specpath', script_dir,
        spec_file
    ], check=True)
    
    print(f"\n✓ Executable built successfully!")
    print(f"  Location: {os.path.join(output_dir, 'WindowsAutomationToolkit.exe')}")
    print(f"  Size: {os.path.getsize(os.path.join(output_dir, 'WindowsAutomationToolkit.exe')) / (1024*1024):.1f} MB")

if __name__ == '__main__':
    build_executable()
