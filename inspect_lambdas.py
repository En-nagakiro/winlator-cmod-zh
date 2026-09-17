import os
import re

base = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui\settings'
for f in sorted(os.listdir(base)):
    if f.startswith('ComposableSingletons$SettingsComposeHostKt$lambda-'):
        p = os.path.join(base, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
            c = fl.read()
            for m in re.finditer(r'const(?:/high16)?\s+[vp]\d+,\s+(0x7f[0-9a-fA-F]+)', c):
                print(f'{f}: {m.group(1)}')
