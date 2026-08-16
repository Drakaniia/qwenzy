from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../src', 'src'),
        ('../src/config', 'src/config'),
        ('../src/modules', 'src/modules'),
        ('../src/utils', 'src/utils'),
    ],
    hiddenimports=[
        'src.tui.app',
        'src.tui.services',
        'src.config.settings',
        'src.utils.system',
        'src.modules.debloat',
        'src.modules.windows_settings',
        'src.modules.power',
        'src.modules.autohotkey',
    ] + collect_submodules('src') + collect_submodules('textual'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WindowsToolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Icon removed - TODO: Create assets/toolkit.ico and uncomment
    # icon='../assets/toolkit.ico',
)

# Note: The executable name matches the public GitHub release asset name.
