import os
import re

base = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui'

for folder in ['container', 'shortcut', 'library', 'dialog']:
    fpath = os.path.join(base, folder)
    if not os.path.exists(fpath):
        continue
    for root, dirs, files in os.walk(fpath):
        for f in files:
            if f.endswith('.smali') and not '$' in f: # main kt files
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    c = fl.read()
                    matches = []
                    for m in re.finditer(r'const-string(?:/jumbo)?\s+[vp]\d+,\s+"([^"]+)"', c):
                        s = m.group(1)
                        if (len(s) > 2 and 
                            not s.startswith('com.') and 
                            not s.startswith('android') and 
                            not s.startswith('kotlin') and 
                            not s.startswith('CC(') and
                            not s.startswith('Lcom/') and
                            not s.endswith('.json') and
                            not s.endswith('.so') and
                            not s.endswith('.tzst') and
                            not s.endswith('.dll') and
                            any(w in s for w in ['Settings', 'Container', 'Shortcut', 'General', 'Video', 'Input', 'Advanced', 'Save', 'Cancel', 'Delete', 'Add', 'Edit'])):
                            matches.append(s)
                    if matches:
                        print(f"{folder}/{f}: {matches}")
