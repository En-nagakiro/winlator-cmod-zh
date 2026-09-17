import os

base = r'apk_dex_smali\smali_classes3\com\winlator\cmod'
for root, dirs, files in os.walk(base):
    for fl in files:
        if fl.endswith('.smali'):
            p = os.path.join(root, fl)
            with open(p, 'r', encoding='utf-8', errors='ignore') as ffl:
                c = ffl.read()
                if 'LibraryFilter' in c:
                    print(os.path.relpath(p, base))
