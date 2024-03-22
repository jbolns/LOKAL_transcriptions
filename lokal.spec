# -*- mode: python ; coding: utf-8 -*-

add_files = [
  ('./images', './images'),
  ('./models/diarization', './models/diarization'),
  ('./models/embedding', './models/embedding'),
  ('./models/segmentation', './models/segmentation'),
  ('./utils/apache_terms.txt', './utils'),
  ('./utils/credits.txt', './utils'),
  ('./utils/view_mode.txt', './utils'),
  ('./utils/key.txt', './utils'),
  ('./utils/license.txt', './utils'),
  ('./utils/try.txt', './utils'),
  ('.venv\Lib\site-packages\whisper', './whisper'),
  ('.venv\Lib\site-packages\pyannote', './pyannote'),
  ('.venv\Lib\site-packages/faster_whisper', './faster_whisper'),
  ('.venv\Lib\site-packages/faster_whisper-0.10.0-py3.11.egg-info', './faster_whisper-0.10.0-py3.11.egg-info'),
  ('.venv\Lib\site-packages\pydub', './pydub'),
  ('.venv\Lib\site-packages\pydub-0.25.1.dist-info', './pydub-0.25.1.dist-info'),
  ('.venv\Lib\site-packages\lightning_fabric', './lightning_fabric'),
  ('.venv\Lib\site-packages/rich', './rich'),
  ('.venv\Lib\site-packages/rich-13.7.0.dist-info', './rich-13.7.0.dist-info'),
  ('.venv\Lib\site-packages\speechbrain', './speechbrain'),
  ('.venv\Lib\site-packages\speechbrain-0.5.16.dist-info', './speechbrain-0.5.16.dist-info'),
  ('.venv\Lib\site-packages/asteroid_filterbanks', './asteroid_filterbanks'),
  ('.venv\Lib\site-packages/asteroid_filterbanks-0.4.0.dist-info', './asteroid_filterbanks-0.4.0.dist-info')
]

exclude_libs = ['yarl', 'tzdata', 'google']

a = Analysis(
  ['main.py'],
  pathex=[],
  binaries=[],
  datas=add_files,
  hiddenimports=[],
  hookspath=[],
  hooksconfig={},
  runtime_hooks=[],
  excludes=exclude_libs,
  noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
  pyz,
  a.scripts,
  [],
  exclude_binaries=True,
  name='run_LOKAL',
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
  icon='./images/icon.ico'
)

coll = COLLECT(
  exe,
  a.binaries,
  a.datas,
  strip=False,
  upx=True,
  upx_exclude=[],
  name='LOKAL_V1_Windows_Multifile',
)
