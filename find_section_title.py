import os
import re

settings_dir = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui\settings'
for f in sorted(os.listdir(settings_dir)):
    if f.endswith('.smali'):
        path = os.path.join(settings_dir, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            lines = fp.readlines()
        for i, line in enumerate(lines):
            if 'SectionTitle' in line:
                print(f"{f}:{i+1}: {line.strip()}")
                # print previous 5 lines
                for j in range(max(0, i-5), i):
                    print(f"   {lines[j].strip()}")
