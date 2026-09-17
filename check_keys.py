import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

tree_zh = ET.parse(r'ludashi_src\res\values-zh-rCN\strings.xml')
zh_strings = {c.attrib['name']: c.text for c in tree_zh.getroot() if 'name' in c.attrib}

tree_en = ET.parse(r'ludashi_src\res\values\strings.xml')
en_strings = {c.attrib['name']: c.text for c in tree_en.getroot() if 'name' in c.attrib}

check_keys = [
    'winlator_path', 'enable_wine_debug', 'enable_box64_logs', 'enable_file_provider',
    'open_with_android_browser', 'share_android_clipboard', 'pause_resume_wine',
    'high_refresh_rate', 'remove_loading_bar_when_booting_games', 'reinstall_imagefs',
    'cursor_speed', 'box64_preset', 'fexcore_preset', 'stability', 'compatibility',
    'intermediate', 'performance', 'sound', 'logs', 'experimental', 'imagefs',
    'appearance', 'environments', 'presets', 'path_settings', 'big_picture_mode',
    'about'
]

for k in check_keys:
    en_val = en_strings.get(k)
    zh_val = zh_strings.get(k)
    print(f"{k}:")
    print(f"   EN: {repr(en_val)}")
    print(f"   ZH: {repr(zh_val)}")
