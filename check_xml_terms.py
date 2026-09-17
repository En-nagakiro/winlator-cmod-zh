import xml.etree.ElementTree as ET
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

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
]

def check_xml(path):
    print(f"\n--- Checking {path} ---")
    if not os.path.exists(path):
        print("File not found!")
        return
    tree = ET.parse(path)
    root = tree.getroot()
    # Map name to text
    str_map = {}
    for child in root:
        name = child.attrib.get('name')
        if name:
            str_map[name] = child.text
    
    for t in terms:
        # Check if t is value or substring
        matches = [k for k, v in str_map.items() if v and t.lower() in v.lower()]
        if matches:
            print(f"  Found '{t}' in {matches} -> {str_map[matches[0]]}")
        else:
            print(f"  NOT FOUND: '{t}'")

check_xml(r'ludashi_src\res\values\strings.xml')
check_xml(r'ludashi_src\res\values-zh-rCN\strings.xml')
check_xml(r'ludashi_src\res\values-zh\strings.xml')
check_xml(r'ludashi_src\res\values\arrays.xml')
check_xml(r'ludashi_src\res\values-zh-rCN\arrays.xml')
