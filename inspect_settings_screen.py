import os
import re

base = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui\settings'
for f in sorted(os.listdir(base)):
    if 'SettingsScreen$2$1$1$' in f:
        p = os.path.join(base, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
            c = fl.read()
            strings = []
            for m in re.finditer(r'const-string(?:/jumbo)?\s+[vp]\d+,\s+"([^"]+)"', c):
                s = m.group(1)
                if not s.startswith('com.winlator') and not s.startswith('CC('):
                    strings.append(s)
            res_ids = []
            for m in re.finditer(r'const\s+[vp]\d+,\s+(0x7f\w+)', c):
                res_ids.append(m.group(1))
            print(f"=== {f} ===")
            if strings:
                print("  Strings:", strings)
            if res_ids:
                print("  Res IDs:", res_ids)
