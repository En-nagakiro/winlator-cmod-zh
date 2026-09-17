import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')

apk_path = r'待汉化\winlator_wineserver_unsigned.apk'
z = zipfile.ZipFile(apk_path)

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
    'Lock screen orientation',
    'Add games',
    'EXTERNAL CONTROLLERS'
]

print("Scanning entries in winlator_wineserver_unsigned.apk ...")
for item in z.namelist():
    if item.endswith('.dex') or item.endswith('.arsc') or item.startswith('res/'):
        data = z.read(item)
        found = []
        for t in terms:
            if t.encode('utf-8') in data or t.encode('utf-16le') in data:
                found.append(t)
        if found:
            print(f"In {item}: {found}")
