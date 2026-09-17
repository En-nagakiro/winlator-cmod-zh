import os
import re

print("=== Checking references to string IDs in smali ===")
string_ids = [
    'winlator_path', 'enable_wine_debug', 'enable_box64_logs', 'enable_file_provider',
    'open_with_android_browser', 'share_android_clipboard', 'pause_resume_wine',
    'high_refresh_rate', 'remove_loading_bar_when_booting_games', 'reinstall_imagefs',
    'cursor_speed', 'box64_preset', 'fexcore_preset', 'stability', 'compatibility',
    'intermediate', 'performance', 'sound', 'logs', 'experimental', 'imagefs'
]

# Find the R$string values for these
r_string_file = r'apk_dex_smali\smali\com\winlator\R$string.smali'
r_map = {}
if os.path.exists(r_string_file):
    with open(r_string_file, 'r', encoding='utf-8') as f:
        for line in f:
            for sid in string_ids:
                if f"field public static final {sid}:I = " in line:
                    val = line.split('=')[-1].strip()
                    r_map[sid] = val
                    print(f"R.string.{sid} = {val}")

# Also check public.xml
public_xml = r'ludashi_src\res\values\public.xml'
if os.path.exists(public_xml):
    with open(public_xml, 'r', encoding='utf-8') as f:
        for line in f:
            for sid in string_ids:
                if f'type="string" name="{sid}"' in line:
                    # extract id="0x..."
                    m = re.search(r'id="(0x[0-9a-fA-F]+)"', line)
                    if m:
                        r_map[sid] = m.group(1)
                        print(f"public.xml string {sid} = {m.group(1)}")
