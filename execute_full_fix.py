import os
import re
import shutil
import xml.etree.ElementTree as ET
from build_complete_translations import translations

# Base directory
base_dir = r'a:\WorkSpace\sep 15,2026,winlator'
ludashi_src = os.path.join(base_dir, 'ludashi_src')
res_dir = os.path.join(ludashi_src, 'res')

# 1. Define new strings to add
new_en_strings = {
    "environment": "Environment",
    "drivers": "Drivers",
    "components": "Components",
    "click_to_upload_custom_cover_art": "Click to upload custom cover art",
    "youtube": "YouTube",
    "mp3": "MP3",
    "folder": "Folder",
    "more_options": "More options",
    "paste": "Paste",
    "help_steamgrid": "SteamGrid API Key",
}

new_zh_strings = {
    "environment": "环境变量",
    "drivers": "驱动",
    "components": "组件",
    "click_to_upload_custom_cover_art": "点击上传自定义封面图",
    "youtube": "YouTube 链接",
    "mp3": "本地 MP3",
    "folder": "本地图片目录",
    "more_options": "更多选项",
    "paste": "粘贴",
    "help_steamgrid": "SteamGrid API 密钥",
}

def escape_xml(val):
    if val.startswith('"') and val.endswith('"'):
        return val
    # If it contains &lt; or &gt; or tags
    val = val.replace('&', '&amp;') if '&amp;' not in val and '&lt;' not in val else val
    # Android strings require escaping unescaped ' with \' or enclosing in "
    if "'" in val and not (val.startswith('"') and val.endswith('"')):
        val = val.replace("'", "\\'")
    if val.startswith(' ') or val.endswith(' '):
        val = f'"{val}"'
    return val

print("=== 1. Updating res/values/strings.xml ===")
en_strings_file = os.path.join(res_dir, 'values', 'strings.xml')
with open(en_strings_file, 'r', encoding='utf-8') as f:
    en_content = f.read()

pattern = re.compile(r'<string\s+name="([^"]+)"(?:\s+formatted="false")?>(.*?)</string>', re.DOTALL)
existing_en = dict(pattern.findall(en_content))

new_en_lines = []
for k, v in sorted(new_en_strings.items()):
    if k not in existing_en:
        extra_attr = ' formatted="false"' if '%' in v and not re.search(r'%\d+\$[sdf%]', v) and not re.search(r'%[sdf%]', v) else ''
        new_en_lines.append(f'    <string name="{k}"{extra_attr}>{escape_xml(v)}</string>')
        print(f"  Added EN key: {k} -> {v}")
    else:
        print(f"  EN key already exists: {k}")

if new_en_lines:
    en_content = en_content.replace('</resources>', '\n'.join(new_en_lines) + '\n</resources>')
    with open(en_strings_file, 'w', encoding='utf-8') as f:
        f.write(en_content)
    print("Saved res/values/strings.xml")

print("\n=== 2. Updating res/values-zh-rCN/strings.xml ===")
zh_strings_file = os.path.join(res_dir, 'values-zh-rCN', 'strings.xml')
with open(zh_strings_file, 'r', encoding='utf-8') as f:
    zh_content = f.read()

existing_zh = dict(pattern.findall(zh_content))
all_zh = dict(translations)
all_zh.update(existing_zh)
all_zh.update(new_zh_strings)

lines = ['<?xml version="1.0" encoding="utf-8"?>\n<resources>']
for k in sorted(all_zh.keys()):
    v = all_zh[k]
    extra_attr = ''
    if '%' in v and not re.search(r'%\d+\$[sdf%]', v) and not re.search(r'%[sdf%]', v):
        extra_attr = ' formatted="false"'
    lines.append(f'    <string name="{k}"{extra_attr}>{escape_xml(v)}</string>')
lines.append('</resources>\n')

zh_final_content = '\n'.join(lines)
with open(zh_strings_file, 'w', encoding='utf-8') as f:
    f.write(zh_final_content)
print(f"Wrote {len(all_zh)} strings to res/values-zh-rCN/strings.xml")

print("\n=== 3. Updating res/values-zh-rCN/arrays.xml ===")
zh_arrays_file = os.path.join(res_dir, 'values-zh-rCN', 'arrays.xml')
zh_arrays_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string-array name="startup_selection_entries">
        <item>正常 (加载所有服务)</item>
        <item>精简 (仅加载必要服务)</item>
        <item>激进 (启动时停止服务)</item>
    </string-array>
    <string-array name="desktop_theme_entries">
        <item>浅色</item>
        <item>深色</item>
    </string-array>
    <string-array name="wincomponent_entries">
        <item>内置 (Wine)</item>
        <item>原生 (Windows)</item>
    </string-array>
    <string-array name="desktop_background_type_entries">
        <item>壁纸图片</item>
        <item>纯色背景</item>
    </string-array>
    <string-array name="touchscreenInputModesEntries">
        <item>触控板</item>
        <item>模拟触摸屏</item>
        <item>直接触摸</item>
    </string-array>
    <string-array name="transformCapturedPointerEntries">
        <item>否</item>
        <item>顺时针</item>
        <item>逆时针</item>
        <item>上下颠倒</item>
        <item>自动 (适用于触控板)</item>
    </string-array>
    <string-array name="binding_type_entries">
        <item>键盘</item>
        <item>鼠标</item>
        <item>手柄</item>
    </string-array>
    <string-array name="device_memory_entries">
        <item>0 (默认)</item>
        <item>512 MB</item>
        <item>1024 MB</item>
        <item>2048 MB</item>
        <item>4096 MB</item>
        <item>8192 MB</item>
        <item>12288 MB</item>
        <item>16384 MB</item>
    </string-array>
    <string-array name="dxvk_framerate_entries">
        <item>0 (默认)</item>
        <item>20</item>
        <item>30</item>
        <item>40</item>
        <item>50</item>
        <item>60</item>
        <item>70</item>
        <item>80</item>
        <item>90</item>
        <item>100</item>
        <item>110</item>
        <item>120</item>
    </string-array>
    <string-array name="dxvk_max_device_memory_entries">
        <item>0 (默认)</item>
        <item>512 MB</item>
        <item>1024 MB</item>
        <item>2048 MB</item>
        <item>4096 MB</item>
    </string-array>
</resources>
'''
with open(zh_arrays_file, 'w', encoding='utf-8') as f:
    f.write(zh_arrays_content)
print("Wrote res/values-zh-rCN/arrays.xml")

print("\n=== 4. Mirroring to res/values-zh/ for universal Chinese fallback ===")
zh_generic_dir = os.path.join(res_dir, 'values-zh')
os.makedirs(zh_generic_dir, exist_ok=True)
with open(os.path.join(zh_generic_dir, 'strings.xml'), 'w', encoding='utf-8') as f:
    f.write(zh_final_content)
with open(os.path.join(zh_generic_dir, 'arrays.xml'), 'w', encoding='utf-8') as f:
    f.write(zh_arrays_content)
print("Created res/values-zh/strings.xml and arrays.xml")

print("\n=== 5. Applying XML layout replacements ===")
replacements = [
    # 5.1 landscape Big Picture Activity (previously completely missed!)
    (os.path.join(res_dir, 'layout-land', 'big_picture_activity.xml'), [
        ('android:text="Click to upload custom cover art"', 'android:text="@string/click_to_upload_custom_cover_art"'),
        ('android:contentDescription="Settings"', 'android:contentDescription="@string/settings"'),
        ('android:text="Settings"', 'android:text="@string/settings"'),
        ('android:text="Graphics Driver:"', 'android:text="@string/graphics_driver"'),
        ('android:text="Driver Version:"', 'android:text="@string/driver_version"'),
        ('android:text="DX Wrapper:"', 'android:text="@string/dx_wrapper"'),
        ('android:text="DXVK/VKD3D Config:"', 'android:text="@string/dxvk_vkd3d_config"'),
        ('android:text="Audio Driver:"', 'android:text="@string/audio_driver"'),
        ('android:text="Box64 Preset:"', 'android:text="@string/box64_preset"'),
        ('android:text="Nothing here. Launch your container and create a Shortcut to get started!"', 'android:text="@string/big_picture_empty_hint"'),
        ('android:contentDescription="Back"', 'android:contentDescription="@string/back"'),
        ('android:text="Back"', 'android:text="@string/back"'),
        ('android:text="YouTube Video URL (Not all YouTube Videos are supported):"', 'android:text="@string/youtube_video_url"'),
        ('android:hint="Enter YouTube URL"', 'android:hint="@string/enter_youtube_url"'),
        ('android:text="Set BG Music"', 'android:text="@string/set_bg_music"'),
        ('android:text="Select MP3"', 'android:text="@string/select_mp3"'),
        ('android:text="Reset MP3"', 'android:text="@string/reset_mp3"'),
        ('android:text="Select Music Source:"', 'android:text="@string/select_music_source"'),
        ('android:text="YouTube"', 'android:text="@string/youtube"'),
        ('android:text="MP3"', 'android:text="@string/mp3"'),
        ('android:text="Disable BG Music"', 'android:text="@string/disable_bg_music"'),
        ('android:text="Background settings:"', 'android:text="@string/background_settings"'),
        ('android:text="Custom Wallpaper"', 'android:text="@string/custom_wallpaper"'),
        ('android:text="Select Wallpaper"', 'android:text="@string/select_wallpaper"'),
        ('android:text="No Background"', 'android:text="@string/no_background"'),
        ('android:text="Wave"', 'android:text="@string/bg_wave"'),
        ('android:text="Gear"', 'android:text="@string/bg_gear"'),
        ('android:text="Quilt"', 'android:text="@string/bg_quilt"'),
        ('android:text="Folder"', 'android:text="@string/folder"'),
        ('android:text="Select Animation (*.png) Folder"', 'android:text="@string/select_anim_folder"'),
        ('android:text="Parallax Mode:"', 'android:text="@string/parallax_mode"'),
        ('android:text="Off"', 'android:text="@string/parallax_off"'),
        ('android:text="Slow"', 'android:text="@string/parallax_slow"'),
        ('android:text="Default"', 'android:text="@string/parallax_default"'),
        ('android:text="Fast"', 'android:text="@string/parallax_fast"'),
        ('android:text="Animation Speed:"', 'android:text="@string/animation_speed"'),
    ]),
    # 5.2 portrait Big Picture Activity
    (os.path.join(res_dir, 'layout', 'big_picture_activity.xml'), [
        ('android:contentDescription="Settings"', 'android:contentDescription="@string/settings"'),
        ('android:contentDescription="Back"', 'android:contentDescription="@string/back"'),
        ('android:text="YouTube"', 'android:text="@string/youtube"'),
        ('android:text="MP3"', 'android:text="@string/mp3"'),
        ('android:text="Folder"', 'android:text="@string/folder"'),
    ]),
    # 5.3 container_detail_fragment tabs
    (os.path.join(res_dir, 'layout', 'container_detail_fragment.xml'), [
        ('<com.google.android.material.tabs.TabItem android:layout_width="fill_parent" android:layout_height="wrap_content" android:text="General" />',
         '<com.google.android.material.tabs.TabItem android:layout_width="fill_parent" android:layout_height="wrap_content" android:text="@string/general" />'),
        ('<com.google.android.material.tabs.TabItem android:layout_width="fill_parent" android:layout_height="wrap_content" android:text="Environment" />',
         '<com.google.android.material.tabs.TabItem android:layout_width="fill_parent" android:layout_height="wrap_content" android:text="@string/environment" />'),
        ('<com.google.android.material.tabs.TabItem android:layout_width="fill_parent" android:layout_height="wrap_content" android:text="Drivers" />',
         '<com.google.android.material.tabs.TabItem android:layout_width="fill_parent" android:layout_height="wrap_content" android:text="@string/drivers" />'),
        ('<com.google.android.material.tabs.TabItem android:layout_width="fill_parent" android:layout_height="wrap_content" android:text="Components" />',
         '<com.google.android.material.tabs.TabItem android:layout_width="fill_parent" android:layout_height="wrap_content" android:text="@string/components" />'),
    ]),
    # 5.4 custom dialog
    (os.path.join(res_dir, 'layout', 'custom_dialog.xml'), [
        ('android:text=" Ok "', 'android:text="@string/ok"'),
        ('android:text="Ok"', 'android:text="@string/ok"'),
    ]),
    # 5.5 file_manager_fragment.xml
    (os.path.join(res_dir, 'layout', 'file_manager_fragment.xml'), [
        ('android:contentDescription="Up Directory"', 'android:contentDescription="@string/up_directory"'),
        ('android:text="Storage"', 'android:text="@string/storage"'),
        ('android:contentDescription="Paste"', 'android:contentDescription="@string/paste"'),
    ]),
    # 5.6 layout-land/file_manager_fragment.xml
    (os.path.join(res_dir, 'layout-land', 'file_manager_fragment.xml'), [
        ('android:contentDescription="Up Directory"', 'android:contentDescription="@string/up_directory"'),
        ('android:text="Storage"', 'android:text="@string/storage"'),
        ('android:contentDescription="Paste"', 'android:contentDescription="@string/paste"'),
    ]),
    # 5.7 main_menu_header.xml
    (os.path.join(res_dir, 'layout', 'main_menu_header.xml'), [
        ('android:text="Storage"', 'android:text="@string/storage"'),
    ]),
    # 5.8 main_menu_storage_footer.xml
    (os.path.join(res_dir, 'layout', 'main_menu_storage_footer.xml'), [
        ('android:text="Storage"', 'android:text="@string/storage"'),
    ]),
    # 5.9 process_info_list_item.xml
    (os.path.join(res_dir, 'layout', 'process_info_list_item.xml'), [
        ('android:contentDescription="More options"', 'android:contentDescription="@string/more_options"'),
    ]),
]

for file_path, pairs in replacements:
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found!")
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    replaced_count = 0
    for target, rep in pairs:
        if target in content:
            content = content.replace(target, rep)
            replaced_count += 1
        else:
            print(f"  Note: '{target}' not in {os.path.basename(file_path)}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {os.path.relpath(file_path, ludashi_src)}: {replaced_count}/{len(pairs)} replaced")

print("\n=== 6. Patching all smali Jetpack Compose UI strings ===")
smali_base = os.path.join(base_dir, 'apk_dex_smali', 'smali_classes3', 'com', 'winlator', 'cmod')

smali_patches = [
    # 1. Settings Section Headers & Dialogs
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-1$1.smali', [
        ('const-string p1, "APPEARANCE"', 'const-string p1, "界面外观"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-3$1.smali', [
        ('const-string p1, "ENVIRONMENTS"', 'const-string p1, "运行环境"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-4$1.smali', [
        ('const-string p1, "PRESETS"', 'const-string p1, "预设方案"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-6$1.smali', [
        ('const-string p1, "PATH SETTINGS"', 'const-string p1, "路径设置"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-7$1.smali', [
        ('const-string p1, "BIG PICTURE MODE"', 'const-string p1, "大屏/手柄模式"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-12$1.smali', [
        ('const-string p1, "ABOUT"', 'const-string p1, "关于"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-13$1.smali', [
        ('const-string v0, "Preset actions"', 'const-string v0, "预设操作"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-14$1.smali', [
        ('const-string v0, "Create new"', 'const-string v0, "新建"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-16$1.smali', [
        ('const-string v0, "Clone"', 'const-string v0, "克隆"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-18$1.smali', [
        ('const-string v0, "Edit"', 'const-string v0, "编辑"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-20$1.smali', [
        ('const-string v0, "Delete"', 'const-string v0, "删除"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-22$1.smali', [
        ('const-string v0, "Apply"', 'const-string v0, "应用"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-23$1.smali', [
        ('const-string v0, "Cancel"', 'const-string v0, "取消"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-24$1.smali', [
        ('const-string v4, "Wine debug channels"', 'const-string v4, "Wine 调试通道"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-25$1.smali', [
        ('const-string v0, "Search channels"', 'const-string v0, "搜索通道..."')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-27$1.smali', [
        ('const-string v0, "Install SoundFont"', 'const-string v0, "安装 SoundFont 音色库"')
    ]),
    ('ui/settings/ComposableSingletons$SettingsComposeHostKt$lambda-28$1.smali', [
        ('const-string v0, "Save"', 'const-string v0, "保存"')
    ]),
    ('ui/settings/SettingsComposeHostKt.smali', [
        ('const-string v10, "Wine debug channels"', 'const-string v10, "Wine 调试通道"')
    ]),

    # 2. Settings Screen rows
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$1.smali', [
        ('const-string v0, "Containers"', 'const-string v0, "容器管理"'),
        ('const-string v2, "Create and manage Windows environments"', 'const-string v2, "创建并管理 Windows 运行环境"')
    ]),
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$2.smali', [
        ('const-string v0, "Components"', 'const-string v0, "组件管理"'),
        ('const-string v2, "Wine, Proton, DXVK, VKD3D and runtimes"', 'const-string v2, "Wine、Proton、DXVK、VKD3D 及运行库"')
    ]),
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$5.smali', [
        ('const-string v0, "Winlator Path"', 'const-string v0, "Winlator 根目录"')
    ]),
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$6.smali', [
        ('const-string v0, "Shortcut Export Path"', 'const-string v0, "快捷方式导出路径"')
    ]),
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$7$1.smali', [
        ('const-string v0, "Enable Big Picture Mode on App Launch"', 'const-string v0, "启动应用时默认进入大屏模式"'),
        ('const-string v0, "Set SteamGrid API Key? (Cover Art)"', 'const-string v0, "设置 SteamGrid API 密钥 (封面图)"')
    ]),
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$8.smali', [
        ('const-string v0, "SteamGridDB API Key"', 'const-string v0, "SteamGridDB API 密钥"')
    ]),
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$9$1.smali', [
        ('const-string v0, "Capture External Pointer"', 'const-string v0, "捕获外部鼠标指针"'),
        ('const-string v0, "Disable Xinput (Used for Exclusive M/KB support)"', 'const-string v0, "禁用 XInput (用于独占键鼠支持)"')
    ]),
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$12.smali', [
        ('const-string v0, "Downloadable Contents URL"', 'const-string v0, "可下载资源 URL 地址"')
    ]),
    ('ui/settings/SettingsComposeHostKt$SettingsScreen$2$1$1$14.smali', [
        ('const-string v0, "About"', 'const-string v0, "关于 Winlator"')
    ]),

    # 3. Theme Types & Sheet
    ('ui/theme/WinlatorThemeType.smali', [
        ('const-string v4, "White"', 'const-string v4, "浅色 (White)"'),
        ('const-string v5, "Bright surfaces with dark text"', 'const-string v5, "清晰高对比度浅色主题"'),
        ('const-string v11, "Black"', 'const-string v11, "深色 (Black)"'),
        ('const-string v12, "Balanced dark theme \\u00b7 Default"', 'const-string v12, "柔和平衡深色主题 · 默认"'),
        ('const-string v5, "AMOLED"', 'const-string v5, "纯黑 (AMOLED)"'),
        ('const-string v6, "Pure black background for OLED displays"', 'const-string v6, "适用于 OLED 屏幕的极致省电纯黑主题"'),
        ('const-string v11, "Blue"', 'const-string v11, "深蓝 (Blue)"'),
        ('const-string v12, "Dark interface with cool blue accents"', 'const-string v12, "深邃午夜蓝点缀暗色主题"'),
        ('const-string v5, "Red"', 'const-string v5, "暗红 (Red)"'),
        ('const-string v6, "Dark interface with warm red accents"', 'const-string v6, "酷炫暗红微调暗色主题"'),
        ('const-string v11, "Purple"', 'const-string v11, "暗紫 (Purple)"'),
        ('const-string v12, "Dark interface with rich purple accents"', 'const-string v12, "奢华深紫微调暗色主题"'),
    ]),
    ('ui/theme/WinlatorThemePickerKt$WinlatorThemePreferenceCard$4.smali', [
        ('const-string v1, "Appearance"', 'const-string v1, "界面外观"'),
        ('const-string v1, "Choose the Winlator theme. Changes are applied immediately."', 'const-string v1, "选择 Winlator 主题，更改将立即生效。"')
    ]),

    # 4. Input Controls Screen
    ('ui/inputcontrols/ComposableSingletons$InputControlsComposeHostKt$lambda-1$1.smali', [
        ('const-string p1, "EXTERNAL CONTROLLERS"', 'const-string p1, "外部控制器"')
    ]),
    ('ui/inputcontrols/ComposableSingletons$InputControlsComposeHostKt$lambda-3$1.smali', [
        ('const-string p1, "EXTERNAL CONTROLLERS"', 'const-string p1, "外部控制器"')
    ]),
    ('ui/inputcontrols/ComposableSingletons$InputControlsComposeHostKt$lambda-5$1.smali', [
        ('const-string v0, "Import"', 'const-string v0, "导入"')
    ]),
    ('ui/inputcontrols/ComposableSingletons$InputControlsComposeHostKt$lambda-6$1.smali', [
        ('const-string v0, "Export"', 'const-string v0, "导出"')
    ]),
    ('ui/inputcontrols/ComposableSingletons$InputControlsComposeHostKt$lambda-7$1.smali', [
        ('const-string v0, "Controls Editor"', 'const-string v0, "按键编辑器"')
    ]),
    ('ui/inputcontrols/ComposableSingletons$InputControlsComposeHostKt$lambda-8$1.smali', [
        ('const-string v0, "-- Select Profile --"', 'const-string v0, "-- 选择配置方案 --"')
    ]),
    ('ui/inputcontrols/ComposableSingletons$InputControlsComposeHostKt$lambda-9$1.smali', [
        ('const-string v1, "No controllers connected"', 'const-string v1, "未连接控制器"')
    ]),
    ('ui/inputcontrols/ComposableSingletons$InputControlsComposeHostKt$lambda-10$1.smali', [
        ('const-string v0, "Remove controller"', 'const-string v0, "移除控制器"')
    ]),
    ('ui/inputcontrols/InputControlsComposeHostKt.smali', [
        ('const-string v1, "Overlay Opacity"', 'const-string v1, "按键透明度"'),
        ('const-string v1, "Profile"', 'const-string v1, "配置方案"'),
        ('const-string v6, "Input Controls"', 'const-string v6, "输入控制"')
    ]),

    # 5. Main Landscape Navigation
    ('ui/LandscapeMainNavigationKt.smali', [
        ('const-string v6, "Library"', 'const-string v6, "游戏库"'),
        ('const-string v6, "Input Controls"', 'const-string v6, "输入控制"'),
        ('const-string v6, "Settings"', 'const-string v6, "设置"')
    ]),

    # 6. Orientation Menu
    ('ui/OrientationOverflowView.smali', [
        ('"Lock screen orientation"', '"锁定屏幕方向"'),
        ('"Vertical mode"', '"竖屏模式"'),
        ('"Horizontal mode"', '"横屏模式"')
    ]),
    ('ShortcutsFragment.smali', [
        ('"Lock screen orientation"', '"锁定屏幕方向"'),
        ('"Vertical mode"', '"竖屏模式"'),
        ('"Horizontal mode"', '"横屏模式"')
    ]),
    ('ui/library/BitmapComposeCompatKt$LibraryOrientationMenu$1$3.smali', [
        ('const-string p3, "Lock screen orientation"', 'const-string p3, "锁定屏幕方向"'),
        ('const-string p3, "Vertical mode"', 'const-string p3, "竖屏模式"'),
        ('const-string p3, "Horizontal mode"', 'const-string p3, "横屏模式"')
    ]),

    # 7. Library Empty State & Chips
    ('ui/library/ComposableSingletons$BitmapComposeCompatKt$lambda-3$1.smali', [
        ('const-string v0, "Add games"', 'const-string v0, "添加游戏"')
    ]),
    ('ui/library/ComposableSingletons$LibraryEmptyStateCompatKt$lambda-2$1.smali', [
        ('const-string v0, "Add games"', 'const-string v0, "添加游戏"')
    ]),
    ('ui/library/LibraryEmptyStateCompatKt.smali', [
        ('const-string v1, "All"', 'const-string v1, "全部"'),
        ('const-string v1, "Favorites"', 'const-string v1, "收藏"'),
        ('const-string v1, "Recent"', 'const-string v1, "最近"')
    ]),

    # 8. CompatibilityRules
    ('ui/settings/CompatibilityRulesKt.smali', [
        ('const-string p0, "Default"', 'const-string p0, "默认"')
    ]),
]

smali_files_count = 0
smali_rep_count = 0
for rel_path, pairs in smali_patches:
    target_path = os.path.join(smali_base, rel_path.replace('/', os.sep))
    if not os.path.exists(target_path):
        print(f"Warning: Smali file {target_path} not found!")
        continue
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()
    replaced_count = 0
    for target, rep in pairs:
        # Strip const-string prefix if specified in pair
        m_prefix = re.match(r'const-string(?:/jumbo)?\s+[vp]\d+,\s*"(.*)"', target)
        clean_target = m_prefix.group(1) if m_prefix else (target[1:-1] if target.startswith('"') and target.endswith('"') else target)
        m_rep_prefix = re.match(r'const-string(?:/jumbo)?\s+[vp]\d+,\s*"(.*)"', rep)
        clean_rep = m_rep_prefix.group(1) if m_rep_prefix else (rep[1:-1] if rep.startswith('"') and rep.endswith('"') else rep)
        
        pattern = re.compile(r'(const-string(?:/jumbo)?\s+[vp]\d+,\s*)"' + re.escape(clean_target) + '"')
        if pattern.search(content):
            content = pattern.sub(r'\1"' + clean_rep + '"', content)
            replaced_count += 1
            smali_rep_count += 1
        elif f'"{clean_target}"' in content:
            content = content.replace(f'"{clean_target}"', f'"{clean_rep}"')
            replaced_count += 1
            smali_rep_count += 1
        else:
            print(f"  Smali note: '{clean_target}' not in {os.path.basename(target_path)}")
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched smali {rel_path}: {replaced_count}/{len(pairs)} replaced")
    smali_files_count += 1

print(f"=== Smali patching complete: {smali_files_count} files, {smali_rep_count} replacements ===")
print("\n=== All updates applied! ===")
