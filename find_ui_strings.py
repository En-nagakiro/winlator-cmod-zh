import os
import re

target_dir = r'apk_dex_smali\smali_classes3\com\winlator\cmod'
exact_strings = [
    'Library', 'All', 'Favorites', 'Recent', 'Add games', 'Input Controls', 'Settings',
    'Lock screen orientation', 'Vertical mode', 'Horizontal mode',
    'Profile', '-- Select Profile --', 'Overlay Opacity', 'Import', 'Export', 'Controls Editor',
    'EXTERNAL CONTROLLERS', 'No controllers connected',
    'APPEARANCE', 'Theme', 'White', 'ENVIRONMENTS', 'Containers', 'Create and manage Windows environments',
    'Appearance', 'Choose the Winlator theme. Changes are applied immediately.',
    'Bright surfaces with dark text', 'Black', 'Balanced dark theme · Default',
    'AMOLED', 'Pure black background for OLED displays',
    'Blue', 'Dark interface with cool blue accents',
    'Red', 'Dark interface with warm red accents',
    'Purple', 'Dark interface with rich purple accents',
    'Components', 'Wine, Proton, DXVK, VKD3D and runtimes',
    'PRESETS', 'Box64 Preset', 'FEXCore Preset', 'Stability', 'Compatibility', 'Intermediate', 'Performance',
    'SOUND', 'Install SoundFont', 'PATH SETTINGS', 'Winlator Path', 'Shortcut Export Path',
    'BIG PICTURE MODE', 'Enable Big Picture Mode on App Launch', 'Set SteamGrid API Key? (Cover Art)',
    'XSERVER', 'Cursor speed', 'Use DRI3 extension', 'Capture External Pointer',
    'Disable Xinput (Used for Exclusive M/KB support)',
    'LOGS', 'Enable Wine debug', 'Wine debug channels', 'Enable Box64 logs',
    'EXPERIMENTAL', 'Enable File Provider', 'Open Android Browser in Wine',
    'Share Android Clipboard with Wine', 'Suspend Wine when app is in background',
    'Enable High Refresh Rate Mode',
    'Search channels', 'Cancel', 'Apply',
    'Remove loading bar when booting games', 'Downloadable Contents URL', 'Save',
    'IMAGEFS', 'Reinstall Imagefs', 'ABOUT', 'About'
]

found_map = {s: [] for s in exact_strings}
for root, dirs, files in os.walk(target_dir):
    for f in files:
        if f.endswith('.smali'):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    c = fl.read()
                    for s in exact_strings:
                        pattern = f'const-string[^\"]*\"{re.escape(s)}\"'
                        if re.search(pattern, c):
                            found_map[s].append(p)
            except Exception as e:
                pass

missing = []
for s in exact_strings:
    if found_map[s]:
        print(f'MATCH: "{s}" -> in {len(found_map[s])} files (e.g. {os.path.basename(found_map[s][0])})')
    else:
        missing.append(s)

print('=== MISSING STRINGS ===')
for m in missing:
    print(' ', m)
