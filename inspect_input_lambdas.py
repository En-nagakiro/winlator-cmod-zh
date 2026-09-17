import os
import re

base = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui\inputcontrols'
for f in sorted(os.listdir(base)):
    if 'ComposableSingletons' in f:
        p = os.path.join(base, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
            c = fl.read()
            for m in re.finditer(r'const-string(?:/jumbo)?\s+[vp]\d+,\s+"([^"]+)"', c):
                s = m.group(1)
                if not s.startswith('com.winlator') and not s.startswith('CC('):
                    print(f'{f}: "{s}"')
