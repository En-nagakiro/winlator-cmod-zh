import os
import re

settings_dir = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui\settings'
print(f"Files in {settings_dir}:")
for f in sorted(os.listdir(settings_dir)):
    if f.endswith('.smali'):
        path = os.path.join(settings_dir, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
        # Find const-string in this file
        strings = re.findall(r'const-string(?:/jumbo)?\s+[vp]\d+,\s*"([^"]+)"', c)
        ui_strings = [s for s in strings if len(s) > 1 and not s.startswith('com.') and not s.startswith('androidx.') and not s.startswith('android.') and not s.endswith('_') and not s.isidentifier()]
        # Also include identifiers that look like words
        word_strings = [s for s in strings if any(w in s.lower() for w in ['box64', 'fexcore', 'preset', 'sound', 'cursor', 'wine', 'environment', 'component', 'container', 'speed', 'manage', 'runtime'])]
        all_s = list(set(ui_strings + word_strings))
        if all_s:
            print(f"\n{f}:")
            for s in all_s:
                print(f"   {repr(s)}")
