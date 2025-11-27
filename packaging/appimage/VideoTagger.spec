# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for VideoTagger AppImage build.
This bundles Python, PyQt6, and all dependencies into a single executable.
"""

import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

# Get the project root directory
project_root = Path(SPECPATH).parent.parent

# Add project root to sys.path so PyInstaller can find the src package
sys.path.insert(0, str(project_root))

block_cipher = None

# Collect all submodules from the src package
src_hiddenimports = collect_submodules('src')

# Collect PyQt6 submodules
pyqt6_hiddenimports = collect_submodules('PyQt6')

a = Analysis(
    [str(project_root / 'main.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=[
        *pyqt6_hiddenimports,
        *src_hiddenimports,
        'PyQt6.sip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VideoTagger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VideoTagger',
)
