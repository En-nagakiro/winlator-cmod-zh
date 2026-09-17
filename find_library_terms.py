import os
import re

base = r'apk_dex_smali\smali_classes3\com\winlator\cmod'
terms = ['Add games', 'Favorites', 'Recent', 'Lock screen orientation', 'Vertical mode', 'Horizontal mode']

for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith('.smali'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                for t in terms:
                    if f'"{t}"' in c:
                        print(f'Term "{t}" in {os.path.relpath(p, base)}')
