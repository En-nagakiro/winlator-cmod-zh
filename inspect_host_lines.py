import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'apk_dex_smali\smali_classes3\com\winlator\cmod\ui\settings\SettingsComposeHostKt.smali', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line for k in ['-title', 'Cursor speed', 'No channels', 'PresetChoiceRow', 'Box64', 'FEXCore']):
        start = max(0, i - 10)
        end = min(len(lines), i + 20)
        print(f"=== Match at line {i}: {line.strip()} ===")
        for j in range(start, end):
            print(f"{j+1}: {lines[j].rstrip()}")
        print("-" * 50)
