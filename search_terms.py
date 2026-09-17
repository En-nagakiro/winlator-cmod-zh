import zipfile
import sys
import glob
import os

sys.stdout.reconfigure(encoding='utf-8')

# Search in apk_dex_smali
print("=== Searching in apk_dex_smali ===")
terms = [
    'Create and manage Windows environments',
    'Wine, Proton, DXVK, VKD3D and runtimes',
    'Winlator Path',
    'LOGS',
    'Enable Wine debug',
    'Enable Box64 logs',
    'EXPERIMENTAL',
    'Enable File Provider',
    'Open Android Browser in Wine',
    'Share Android Clipboard with Wine',
    'Suspend Wine when app is in background',
    'Enable High Refresh Rate Mode',
    'Remove loading bar when booting games',
    'IMAGEFS',
    'Reinstall Imagefs',
    'Cursor speed',
    'Box64 Preset',
    'FEXCore Preset',
    'SOUND',
    'Stability',
    'Compatibility',
    'Intermediate',
    'Performance',
    'Theme'
]

matches = {}
for root, dirs, files in os.walk('apk_dex_smali'):
    for f in files:
        if f.endswith('.smali') or f.endswith('.xml'):
            full = os.path.join(root, f)
            try:
                with open(full, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                for t in terms:
                    if t in content:
                        matches.setdefault(t, []).append(full)
            except Exception:
                pass

for t in terms:
    found = matches.get(t, [])
    print(f"[{len(found)}] {t}:")
    for path in found[:3]:
        print(f"    {path}")
