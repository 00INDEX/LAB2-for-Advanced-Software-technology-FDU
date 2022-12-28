# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py', 'src/__init__.py', 'src/Entity/__init__.py', 'src/Entity/Entity.py', 'src/Entity/Task.py',
    'src/Entity/User/User.py', 'src/Entity/User/Client.py', 'src/Entity/User/Dispatcher.py', 'src/Entity/User/Manager.py',
    'src/Entity/User/Worker.py', 'src/Entity/Action/Action.py','src/Entity/Action/ComplainAction.py', 'src/Entity/Action/DispatchAction.py',
    'src/Entity/Action/ServiceAction.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='main',
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
)
