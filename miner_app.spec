# -*- mode: python ; coding: utf-8 -*- 

# Import necessary PyInstaller modules
from PyInstaller.utils.hooks import collect_submodules

# Collect all the submodules for dependencies
hiddenimports = collect_submodules('PyQt5')  # Collect submodules for PyQt5 if you're using it for the GUI

a = Analysis(
    ['gui.py'],  # Entry point for GUI
    pathex=['./'],  # Path to your project folder
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

# Create the executable using the EXE class
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='miner_app',  # Name of the output executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression (optional, may reduce the file size)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Disable the console window for GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# For GUI version: 
# - We want to make sure PyQt5 or Tkinter (if used) and other GUI components are included.
# - When running the GUI, the PyInstaller package will use the 'gui.py' entry point.
