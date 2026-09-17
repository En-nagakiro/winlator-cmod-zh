import os
import re

folders = ['ui/settings', 'ui/theme', 'ui/library', 'ui/inputcontrols', 'ui/container', 'ui/shortcut']
base = r'apk_dex_smali\smali_classes3\com\winlator\cmod'

for fld in folders:
    fld_path = os.path.join(base, fld.replace('/', '\\'))
    if not os.path.exists(fld_path):
        continue
    print(f'=== Folder: {fld} ===')
    seen = set()
    for root, dirs, files in os.walk(fld_path):
        for f in files:
            if f.endswith('.smali'):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    content = fl.read()
                    for m in re.finditer(r'const-string(?:/jumbo)?\s+[vp]\d+,\s+"([^"]+)"', content):
                        s = m.group(1)
                        if len(s) > 1 and not s.startswith('Lcom/') and not s.startswith('android.') and not s.startswith('androidx.') and not s.startswith('kotlin/') and not s.startswith('CC('):
                            if s not in seen and any(c.isalpha() for c in s):
                                seen.add(s)
                                print(f'  [{f}] "{s}"')
