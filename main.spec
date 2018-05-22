# -*- mode: python -*-

block_cipher = None

added_files = [
    ('resources\\*', 'resources'),
    ('design\\*', 'design'),
]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\Juacy Willian\\workspaces\\python-projects\\protocolos'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Protocolos',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
