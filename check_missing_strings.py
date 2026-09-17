import xml.etree.ElementTree as ET
import os

res_dir = r'ludashi_src\res'
en_strings_path = os.path.join(res_dir, 'values', 'strings.xml')
zh_strings_path = os.path.join(res_dir, 'values-zh-rCN', 'strings.xml')

en_tree = ET.parse(en_strings_path)
en_root = en_tree.getroot()
en_dict = {s.attrib.get('name'): s.text for s in en_root.findall('string')}

zh_tree = ET.parse(zh_strings_path)
zh_root = zh_tree.getroot()
zh_dict = {s.attrib.get('name'): s.text for s in zh_root.findall('string')}

missing_in_zh = [k for k in en_dict if k not in zh_dict]
print(f"Total EN strings: {len(en_dict)}")
print(f"Total ZH strings: {len(zh_dict)}")
print(f"Missing in ZH: {len(missing_in_zh)}")
if missing_in_zh:
    print("Sample missing in ZH:", missing_in_zh[:20])
