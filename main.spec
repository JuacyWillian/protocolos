# -*- mode: python -*-

block_cipher = None

added_files = [('design/*ui', 'design'),
	       ('resources/*.png', 'resources'),]

a = Analysis(['main.py'],
             pathex=['/home/jw/workspaces/python-projects/python_gui_programming'],
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
          console=True )
