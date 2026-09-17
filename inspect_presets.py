import os

with open(r'apk_dex_smali\smali_classes3\com\winlator\cmod\box64\Box64PresetManager.smali', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if '"STABILITY"' in l:
        print(f'Line {i}: {l.strip()}')
        for j in range(max(0, i-5), min(len(lines), i+25)):
            print(f'  {j}: {lines[j].strip()}')
        print('='*40)
