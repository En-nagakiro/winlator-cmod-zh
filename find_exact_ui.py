import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

search_exact = [
    "PATH SETTINGS",
    "BIG PICTURE MODE",
    "XSERVER",
    "LOGS",
    "EXPERIMENTAL",
    "IMAGEFS",
    "ABOUT",
    "Cursor speed",
    "Enable Big Picture Mode on App Launch",
    "Set SteamGrid API Key? (Cover Art)",
    "Use DRI3 extension",
    "Capture External Pointer",
    "Disable Xinput (Used for Exclusive M/KB support)",
    "Wine debug channels",
    "Search channels",
    "Enable High Refresh Rate Mode",
    "Remove loading bar when booting games",
    "Downloadable Contents URL",
    "Reinstall Imagefs",
    "Choose the Winlator theme. Changes are applied immediately.",
    "Bright surfaces with dark text",
    "No controllers connected",
    "Controls Editor",
    "Lock screen orientation",
    "Add games",
    "Box64 Preset",
    "FEXCore Preset"
]

results = {}
for root, dirs, files in os.walk('apk_dex_smali'):
    for f in files:
        if f.endswith('.smali') or f.endswith('.xml'):
            full = os.path.join(root, f)
            try:
                with open(full, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                for s in search_exact:
                    if s in content:
                        results.setdefault(s, []).append(full)
            except Exception:
                pass

for s in search_exact:
    found = results.get(s, [])
    print(f"=== '{s}' ({len(found)} matches) ===")
    for path in found:
        print(f"   {path}")
