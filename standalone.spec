# -*- mode: python -*-

block_cipher = None


a = Analysis(['standalone\\standalone.py'],
             pathex=['standalone', 'lib', 'lib\\torrent2http', 'd:\\Projects\\!MyProjects\\!DEV\\script.module.torrent2http', 'c:\\Python27\\Lib'],
             binaries=[],
             datas=[('addon.xml', '.'), ('d:\\Projects\\!MyProjects\\!DEV\\script.module.torrent2http\\lib\\torrent2http\\remote\\statgui.css', '.'), ('bin\\windows_x86\\torrent2http.exe.size.txt', 'bin\\windows_x86'), ('bin\\windows_x86\\torrent2http.exe', 'bin\\windows_x86'), ('standalone\\settings.xml', '.')],
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
          exclude_binaries=True,
          name='standalone',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='standalone')
