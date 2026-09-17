import os
import re

base = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui\settings'
for f in sorted(os.listdir(base)):
    p = os.path.join(base, f)
    with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
        c = fl.read()
        for m in re.finditer(r'const-string(?:/jumbo)?\s+[vp]\d+,\s+"([^"]+)"', c):
            s = m.group(1)
            if any(k.lower() in s.lower() for k in ['sound', 'xserver', 'dri3', 'logs', 'wine debug', 'box64 log', 'experimental', 'file provider', 'browser', 'clipboard', 'suspend', 'refresh', 'loading bar', 'imagefs', 'stability', 'intermediate', 'performance']):
                print(f'{f}: {s}')
