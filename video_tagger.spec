# video_tagger.spec
# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Get the project root directory
project_root = os.path.abspath(os.path.dirname(__file__))

# Collect PyQt6 related data files (resources only, no Python files)
datas = collect_data_files('PyQt6')

# Collect all PyQt6 submodules (includes QtMultimedia, QtMultimediaWidgets)
hiddenimports = collect_submodules('PyQt6')

# Add application's own modules as hidden imports
hiddenimports += [
    'src',
    'src.ui',
    'src.ui.main_window',
    'src.ui.player',
    'src.ui.settings_dialog',
    'src.core',
    'src.core.video_scanner',
    'src.core.tag_manager',
    'src.core.shortcut_manager',
    'src.utils',
    'src.utils.file_utils',
]

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='video-tagger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression (install with: sudo apt install upx-ucl)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application set to False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
