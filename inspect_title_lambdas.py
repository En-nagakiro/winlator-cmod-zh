import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

settings_dir = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui\settings'
for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
    fname = f"ComposableSingletons$SettingsComposeHostKt$lambda-{i}$1.smali"
    fpath = os.path.join(settings_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()
        print(f"\n=== {fname} ===")
        # Look for const or invoke
        lines = content.split('\n')
        for j, line in enumerate(lines):
            if 'SectionTitle' in line:
                for k in range(max(0, j-10), j+2):
                    print(f"  {lines[k]}")
