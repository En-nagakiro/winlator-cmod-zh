import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

tree_en = ET.parse(r'ludashi_src\res\values\strings.xml')
en_strings = {c.attrib['name']: c.text for c in tree_en.getroot() if 'name' in c.attrib}

tree_zh = ET.parse(r'ludashi_src\res\values-zh-rCN\strings.xml')
zh_strings = {c.attrib['name']: c.text for c in tree_zh.getroot() if 'name' in c.attrib}

missing_in_zh = {}
for k, v in en_strings.items():
    if k not in zh_strings:
        missing_in_zh[k] = v

print(f"Total English strings: {len(en_strings)}")
print(f"Total Chinese strings: {len(zh_strings)}")
print(f"Missing in Chinese: {len(missing_in_zh)}")

print("\n--- Missing strings list ---")
for k, v in sorted(missing_in_zh.items()):
    print(f"{k}: {repr(v)}")
