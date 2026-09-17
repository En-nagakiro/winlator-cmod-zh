import os
import re

base_dir = r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui'

results = {}
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.smali'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                for line_num, line in enumerate(fl, 1):
                    m = re.search(r'const-string(?:/jumbo)?\s+[vp]\d+,\s+"([^"]+)"', line)
                    if m:
                        s = m.group(1)
                        # Filter out internal identifiers, class names, method signatures, keys
                        if (len(s) > 1 and 
                            not s.startswith('com.') and 
                            not s.startswith('androidx.') and 
                            not s.startswith('android.') and 
                            not s.startswith('kotlin') and 
                            not s.startswith('Lcom/') and
                            not s.startswith('CC(') and
                            not s.startswith('$') and
                            not s.endswith('()V') and
                            not s.endswith('()') and
                            not re.match(r'^[a-z0-9_\-]+$', s) and # likely key/id
                            any(c.isalpha() for c in s)):
                            rel = os.path.relpath(p, base_dir)
                            if s not in results:
                                results[s] = []
                            results[s].append((rel, line_num))

print(f"Found {len(results)} potential UI strings in ui/:")
for s in sorted(results.keys()):
    files_str = ", ".join(f"{r}:{ln}" for r, ln in results[s][:3])
    print(f'"{s}": [{files_str}]')
