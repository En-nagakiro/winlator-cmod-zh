import os
import re
import xml.etree.ElementTree as ET
from build_complete_translations import translations

# English mappings for any new keys added
en_layout_strings = {
    "big_picture_mode": "Big Picture Mode",
    "big_picture_empty_hint": "Nothing here. Launch your container and create a Shortcut to get started!",
    "file_manager": "File Manager",
    "change_icon": "Change Icon",
    "clone": "Clone",
    "toggle_relative_mouse_movement": "Toggle Relative Mouse Movement",
    "pause_resume": "Pause/Resume",
    "enter_command": "Enter command",
    "execute": "Execute",
    "rendering": "Rendering",
    "fps_limiter": "FPS Limiter",
    "super_resolution": "Super Resolution",
    "upscaler_mode": "Upscaler Mode",
    "sharpness": "Sharpness",
    "post_effect": "Post Effect",
    "reshade": "ReShade",
    "effect": "Effect",
    "strength": "Strength",
    "frame_generation": "Frame Generation",
    "save_preset": "Save Preset",
    "display_and_effects": "Display and Effects",
    "picture_in_picture": "Picture in Picture",
    "soft_stretch": "Soft Stretch",
    "controls": "Controls",
    "touch_controls_opacity": "Touch Controls Opacity",
    "show_keyboard": "Show Keyboard",
    "relative_mouse": "Relative Mouse",
    "hud": "HUD",
    "enable_hud": "Enable HUD",
    "style": "Style",
    "hud_metrics": "HUD Metrics",
    "fps_metric": "FPS",
    "gpu_metric": "GPU",
    "cpu_metric": "CPU",
    "ram_metric": "RAM",
    "batt_temp_metric": "Batt/Temp",
    "renderer": "Renderer",
    "hud_size": "HUD Size",
    "hud_opacity": "HUD Opacity",
    "reset_hud": "Reset HUD",
    "show_logs": "Show Logs",
    "app_settings_title": "APP SETTINGS",
    "runtime_and_interface": "Runtime and interface",
    "presets_paths_input": "Presets, paths, input and diagnostics",
    "enable_dark_mode": "Enable Dark Mode",
    "winlator_path": "Winlator Path",
    "choose_path": "Choose Path",
    "shortcut_export_path": "Shortcut Export Path",
    "path_settings": "Path Settings",
    "enable_big_picture_on_launch": "Enable Big Picture Mode on App Launch",
    "set_steamgrid_api_key": "Set SteamGrid API Key? (Cover Art)",
    "enter_api_key_here": "Enter your API Key here",
    "steamgrid_api_key": "SteamGridDB API Key",
    "capture_external_pointer": "Capture External Pointer",
    "disable_xinput_summary": "Disable Xinput (Used for Exclusive M/KB support)",
    "downloadable_contents_url": "Downloadable Contents URL",
    "number_of_times_played": "Number of times played: ",
    "playtime": "Playtime: ",
    "reset_properties": "Reset Properties",
    "current_version": "Current Version: ",
    "exclusive_input": "Exclusive Input",
    "present_mode": "Present Mode",
    "renderer_driver": "Renderer Driver",
    "texture_filter": "Texture Filter",
    "swap_red_blue_channels": "Swap red/blue channels",
    "max_frame_latency": "Max Frame Latency",
    "theme_color": "Theme Color",
    "move_mouse_cursor_dragging": "Move mouse cursor while dragging",
    "latest_stevenmxz_drivers": "Latest StevenMXZ Drivers",
    "manage_driver_sources_and_updates": "Manage driver sources and updates.",
    "use_square_deadzone_left": "Use Square Deadzone (Left Stick)",
    "bg_music_settings": "Background Music Settings",
    "youtube_video_url": "YouTube Video URL (Not all YouTube Videos are supported):",
    "enter_youtube_url": "Enter YouTube URL",
    "set_bg_music": "Set BG Music",
    "select_mp3": "Select MP3",
    "reset_mp3": "Reset MP3",
    "select_music_source": "Select Music Source:",
    "disable_bg_music": "Disable BG Music",
    "background_settings": "Background settings:",
    "custom_wallpaper": "Custom Wallpaper",
    "select_wallpaper": "Select Wallpaper",
    "no_background": "No Background",
    "bg_wave": "Wave",
    "bg_gear": "Gear",
    "bg_quilt": "Quilt",
    "select_anim_folder": "Select Animation (*.png) Folder",
    "parallax_mode": "Parallax Mode:",
    "parallax_off": "Off",
    "parallax_slow": "Slow",
    "parallax_default": "Default",
    "parallax_fast": "Fast",
    "animation_speed": "Animation Speed:",
    "emulator_64bit": "64bit Emulator",
    "directinput": "DirectInput",
    "driver_version": "Driver Version:",
    "dx_wrapper": "DX Wrapper:",
    "dxvk_vkd3d_config": "DXVK/VKD3D Config:",
    "back": "Back",
    "new_task_plus": "+ New Task"
}

def escape_xml(val):
    if val.startswith('"') and val.endswith('"'):
        return val
    # If it contains &lt; or &gt; or tags
    val = val.replace('&', '&amp;') if '&amp;' not in val and '&lt;' not in val else val
    # Android strings requires escaping unescaped ' with \' or enclosing in "
    if "'" in val and not (val.startswith('"') and val.endswith('"')):
        val = val.replace("'", "\\'")
    # If val starts with space or has quotes
    if val.startswith(' ') or val.endswith(' '):
        val = f'"{val}"'
    return val

print("1. Updating res/values-zh-rCN/strings.xml...")
zh_strings_file = 'ludashi_src/res/values-zh-rCN/strings.xml'

# Read existing zh strings to preserve them
with open(zh_strings_file, 'r', encoding='utf-8') as f:
    zh_content = f.read()

pattern = re.compile(r'<string\s+name="([^"]+)"(?:\s+formatted="false")?>(.*?)</string>', re.DOTALL)
existing_zh = dict(pattern.findall(zh_content))
print(f"Existing zh-rCN strings count: {len(existing_zh)}")

# Combine existing with new translations
all_zh = dict(existing_zh)
for k, v in translations.items():
    all_zh[k] = v

print(f"Total zh-rCN strings after merge: {len(all_zh)}")

# Build new values-zh-rCN/strings.xml
lines = ['<?xml version="1.0" encoding="utf-8"?>\n<resources>']
for k in sorted(all_zh.keys()):
    v = all_zh[k]
    # Check if formatted="false" is needed
    extra_attr = ''
    if '%' in v and not re.search(r'%\d+\$[sdf%]', v) and not re.search(r'%[sdf%]', v):
        extra_attr = ' formatted="false"'
    lines.append(f'    <string name="{k}"{extra_attr}>{escape_xml(v)}</string>')
lines.append('</resources>\n')

with open(zh_strings_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print("Wrote res/values-zh-rCN/strings.xml successfully!")

print("\n2. Updating res/values/strings.xml with new keys...")
en_strings_file = 'ludashi_src/res/values/strings.xml'
with open(en_strings_file, 'r', encoding='utf-8') as f:
    en_content = f.read()

existing_en = dict(pattern.findall(en_content))
added_en_count = 0
new_en_lines = []
for k, v in sorted(en_layout_strings.items()):
    if k not in existing_en:
        extra_attr = ''
        if '%' in v and not re.search(r'%\d+\$[sdf%]', v) and not re.search(r'%[sdf%]', v):
            extra_attr = ' formatted="false"'
        new_en_lines.append(f'    <string name="{k}"{extra_attr}>{escape_xml(v)}</string>')
        added_en_count += 1

if new_en_lines:
    en_content = en_content.replace('</resources>', '\n'.join(new_en_lines) + '\n</resources>')
    with open(en_strings_file, 'w', encoding='utf-8') as f:
        f.write(en_content)
print(f"Added {added_en_count} new strings to res/values/strings.xml!")

print("\n3. Creating res/values-zh-rCN/arrays.xml...")
zh_arrays_file = 'ludashi_src/res/values-zh-rCN/arrays.xml'
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
</resources>
'''
with open(zh_arrays_file, 'w', encoding='utf-8') as f:
    f.write(zh_arrays_content)
print("Wrote res/values-zh-rCN/arrays.xml successfully!")

print("\n4. Replacing hardcoded strings in layout and menu files...")

replacements = [
    # menus
    ('ludashi_src/res/menu/shortcut_popup_menu.xml', [
        ('android:title="Change Icon"', 'android:title="@string/change_icon"'),
        ('android:title="Export"', 'android:title="@string/export"'),
        ('android:title="Clone"', 'android:title="@string/clone"'),
    ]),
    ('ludashi_src/res/menu/main_menu.xml', [
        ('android:title="File Manager"', 'android:title="@string/file_manager"'),
    ]),
    ('ludashi_src/res/menu/xserver_menu.xml', [
        ('android:title="Toggle Relative Mouse Movement"', 'android:title="@string/toggle_relative_mouse_movement"'),
        ('android:title="Pause/Resume"', 'android:title="@string/pause_resume"'),
    ]),
    ('ludashi_src/res/menu/containers_menu.xml', [
        ('android:title="Big Picture Mode"', 'android:title="@string/big_picture_mode"'),
    ]),
    # layouts
    ('ludashi_src/res/layout/activity_terminal.xml', [
        ('android:hint="Enter command"', 'android:hint="@string/enter_command"'),
        ('android:text="Execute"', 'android:text="@string/execute"'),
    ]),
    ('ludashi_src/res/layout/adrenotools_fragment.xml', [
        ('android:text="Installed Driver"', 'android:text="@string/installed_driver"'),
        ('android:text="Latest StevenMXZ Drivers"', 'android:text="@string/latest_stevenmxz_drivers"'),
        ('android:text="Refresh"', 'android:text="@string/refresh"'),
        ('android:text="Driver Repositories"', 'android:text="@string/driver_repositories"'),
        ('android:text="Manage driver sources and updates."', 'android:text="@string/manage_driver_sources_and_updates"'),
        ('android:text="Install Driver from File"', 'android:text="@string/install_driver_from_file"'),
    ]),
    ('ludashi_src/res/layout/analog_stick_config_dialog.xml', [
        ('android:text="Left Analog Stick Settings"', 'android:text="@string/left_analog_stick_settings"'),
        ('android:text="Use Square Deadzone (Left Stick)"', 'android:text="@string/use_square_deadzone_left"'),
        ('android:text="Right Analog Stick Settings"', 'android:text="@string/right_analog_stick_settings"'),
        ('android:text="Invert X Axis (Left Stick)"', 'android:text="@string/invert_x_axis_left"'),
        ('android:text="Invert Y Axis (Left Stick)"', 'android:text="@string/invert_y_axis_left"'),
        ('android:text="Invert X Axis (Right Stick)"', 'android:text="@string/invert_x_axis_right"'),
        ('android:text="Invert Y Axis (Right Stick)"', 'android:text="@string/invert_y_axis_right"'),
    ]),
    ('ludashi_src/res/layout/container_detail_fragment.xml', [
        ('android:text="Renderer"', 'android:text="@string/renderer"'),
        ('android:text="64bit Emulator"', 'android:text="@string/emulator_64bit"'),
        ('android:text="HUD"', 'android:text="@string/hud"'),
        ('android:text="DirectInput"', 'android:text="@string/directinput"'),
        ('android:text="Exclusive Input"', 'android:text="@string/exclusive_input"'),
    ]),
    ('ludashi_src/res/layout/control_element_settings.xml', [
        ('android:text="Opacity"', 'android:text="@string/opacity"'),
        ('android:text="Theme Color"', 'android:text="@string/theme_color"'),
        ('android:text="Remove"', 'android:text="@string/remove"'),
        ('android:text="Browse…"', 'android:text="@string/browse"'),
        ('android:text="Move mouse cursor while dragging"', 'android:text="@string/move_mouse_cursor_dragging"'),
    ]),
    ('ludashi_src/res/layout/dxvk_config_dialog.xml', [
        ('android:text="Max Frame Latency"', 'android:text="@string/max_frame_latency"'),
    ]),
    ('ludashi_src/res/layout/renderer_options_dialog.xml', [
        ('android:text="Present Mode"', 'android:text="@string/present_mode"'),
        ('android:text="Renderer Driver"', 'android:text="@string/renderer_driver"'),
        ('android:text="Texture Filter"', 'android:text="@string/texture_filter"'),
        ('android:text="Swap red/blue channels"', 'android:text="@string/swap_red_blue_channels"'),
    ]),
    ('ludashi_src/res/layout/shortcut_properties_dialog.xml', [
        ('android:text="Number of times played: "', 'android:text="@string/number_of_times_played"'),
        ('android:text="Playtime: "', 'android:text="@string/playtime"'),
        ('android:text="Reset Properties"', 'android:text="@string/reset_properties"'),
    ]),
    ('ludashi_src/res/layout/shortcut_settings_dialog.xml', [
        ('android:text="Current Version:"', 'android:text="@string/current_version"'),
        ('android:text="Renderer"', 'android:text="@string/renderer"'),
        ('android:text="64bit Emulator"', 'android:text="@string/emulator_64bit"'),
        ('android:text="Enable Relative Mouse"', 'android:text="@string/relative_mouse_movement"'),
        ('android:text="Disable Mouse"', 'android:text="@string/disable_mouse"'),
        ('android:text="Exclusive Input"', 'android:text="@string/exclusive_input"'),
    ]),
    ('ludashi_src/res/layout/wined3d_config_dialog.xml', [
        ('android:text="Renderer"', 'android:text="@string/renderer"'),
    ]),
    ('ludashi_src/res/layout/settings_fragment.xml', [
        ('android:text="APP SETTINGS"', 'android:text="@string/app_settings_title"'),
        ('android:text="Runtime and interface"', 'android:text="@string/runtime_and_interface"'),
        ('android:text="Presets, paths, input and diagnostics"', 'android:text="@string/presets_paths_input"'),
        ('android:text="Enable Dark Mode"', 'android:text="@string/enable_dark_mode"'),
        ('android:text="Theme"', 'android:text="@string/theme"'),
        ('android:text="Winlator Path"', 'android:text="@string/winlator_path"'),
        ('android:text="Choose Path"', 'android:text="@string/choose_path"'),
        ('android:text="Shortcut Export Path"', 'android:text="@string/shortcut_export_path"'),
        ('android:text="Path Settings"', 'android:text="@string/path_settings"'),
        ('android:text="Enable Big Picture Mode on App Launch"', 'android:text="@string/enable_big_picture_on_launch"'),
        ('android:text="Set SteamGrid API Key? (Cover Art)"', 'android:text="@string/set_steamgrid_api_key"'),
        ('android:hint="Enter your API Key here"', 'android:hint="@string/enter_api_key_here"'),
        ('android:text="SteamGridDB API Key"', 'android:text="@string/steamgrid_api_key"'),
        ('android:text="Big Picture Mode"', 'android:text="@string/big_picture_mode"'),
        ('android:text="Capture External Pointer"', 'android:text="@string/capture_external_pointer"'),
        ('android:text="Disable Xinput (Used for Exclusive M/KB support)"', 'android:text="@string/disable_xinput_summary"'),
        ('android:text="Downloadable Contents URL"', 'android:text="@string/downloadable_contents_url"'),
    ]),
    ('ludashi_src/res/layout/big_picture_activity.xml', [
        ('android:text="Settings"', 'android:text="@string/settings"'),
        ('android:text="Graphics Driver:"', 'android:text="@string/graphics_driver"'),
        ('android:text="Driver Version:"', 'android:text="@string/driver_version"'),
        ('android:text="DX Wrapper:"', 'android:text="@string/dx_wrapper"'),
        ('android:text="DXVK/VKD3D Config:"', 'android:text="@string/dxvk_vkd3d_config"'),
        ('android:text="Audio Driver:"', 'android:text="@string/audio_driver"'),
        ('android:text="Box64 Preset:"', 'android:text="@string/box64_preset"'),
        ('android:text="Nothing here. Launch your container and create a Shortcut to get started!"', 'android:text="@string/big_picture_empty_hint"'),
        ('android:text="Back"', 'android:text="@string/back"'),
        ('android:text="YouTube Video URL (Not all YouTube Videos are supported):"', 'android:text="@string/youtube_video_url"'),
        ('android:hint="Enter YouTube URL"', 'android:hint="@string/enter_youtube_url"'),
        ('android:text="Set BG Music"', 'android:text="@string/set_bg_music"'),
        ('android:text="Select MP3"', 'android:text="@string/select_mp3"'),
        ('android:text="Reset MP3"', 'android:text="@string/reset_mp3"'),
        ('android:text="Select Music Source:"', 'android:text="@string/select_music_source"'),
        ('android:text="Disable BG Music"', 'android:text="@string/disable_bg_music"'),
        ('android:text="Background settings:"', 'android:text="@string/background_settings"'),
        ('android:text="Custom Wallpaper"', 'android:text="@string/custom_wallpaper"'),
        ('android:text="Select Wallpaper"', 'android:text="@string/select_wallpaper"'),
        ('android:text="No Background"', 'android:text="@string/no_background"'),
        ('android:text="Wave"', 'android:text="@string/bg_wave"'),
        ('android:text="Gear"', 'android:text="@string/bg_gear"'),
        ('android:text="Quilt"', 'android:text="@string/bg_quilt"'),
        ('android:text="Select Animation (*.png) Folder"', 'android:text="@string/select_anim_folder"'),
        ('android:text="Parallax Mode:"', 'android:text="@string/parallax_mode"'),
        ('android:text="Off"', 'android:text="@string/parallax_off"'),
        ('android:text="Slow"', 'android:text="@string/parallax_slow"'),
        ('android:text="Default"', 'android:text="@string/parallax_default"'),
        ('android:text="Fast"', 'android:text="@string/parallax_fast"'),
        ('android:text="Animation Speed:"', 'android:text="@string/animation_speed"'),
    ]),
    ('ludashi_src/res/layout/left_sidebar_original.xml', [
        ('android:text="Rendering"', 'android:text="@string/rendering"'),
        ('android:text="FPS Limiter"', 'android:text="@string/fps_limiter"'),
        ('android:text="Super Resolution"', 'android:text="@string/super_resolution"'),
        ('android:text="Upscaler Mode"', 'android:text="@string/upscaler_mode"'),
        ('android:text="Sharpness"', 'android:text="@string/sharpness"'),
        ('android:text="Post Effect"', 'android:text="@string/post_effect"'),
        ('android:text="ReShade"', 'android:text="@string/reshade"'),
        ('android:text="Effect"', 'android:text="@string/effect"'),
        ('android:text="Strength"', 'android:text="@string/strength"'),
        ('android:text="Frame Generation"', 'android:text="@string/frame_generation"'),
        ('android:text="Save Preset"', 'android:text="@string/save_preset"'),
        ('android:text="Display and Effects"', 'android:text="@string/display_and_effects"'),
        ('android:text="Picture in Picture"', 'android:text="@string/picture_in_picture"'),
        ('android:text="Toggle Fullscreen"', 'android:text="@string/toggle_fullscreen"'),
        ('android:text="Magnifier"', 'android:text="@string/magnifier"'),
        ('android:text="Soft Stretch"', 'android:text="@string/soft_stretch"'),
        ('android:text="Controls"', 'android:text="@string/controls"'),
        ('android:text="Touch Controls Opacity"', 'android:text="@string/touch_controls_opacity"'),
        ('android:text="Show Keyboard"', 'android:text="@string/show_keyboard"'),
        ('android:text="Vibration"', 'android:text="@string/vibration"'),
        ('android:text="Relative Mouse"', 'android:text="@string/relative_mouse"'),
        ('android:text="Disable Mouse"', 'android:text="@string/disable_mouse"'),
        ('android:text="HUD"', 'android:text="@string/hud"'),
        ('android:text="Enable HUD"', 'android:text="@string/enable_hud"'),
        ('android:text="Style"', 'android:text="@string/style"'),
        ('android:text="HUD Metrics"', 'android:text="@string/hud_metrics"'),
        ('android:text="FPS"', 'android:text="@string/fps_metric"'),
        ('android:text="GPU"', 'android:text="@string/gpu_metric"'),
        ('android:text="CPU"', 'android:text="@string/cpu_metric"'),
        ('android:text="RAM"', 'android:text="@string/ram_metric"'),
        ('android:text="Batt/Temp"', 'android:text="@string/batt_temp_metric"'),
        ('android:text="Renderer"', 'android:text="@string/renderer"'),
        ('android:text="HUD Size"', 'android:text="@string/hud_size"'),
        ('android:text="HUD Opacity"', 'android:text="@string/hud_opacity"'),
        ('android:text="Reset HUD"', 'android:text="@string/reset_hud"'),
        ('android:text="Show Logs"', 'android:text="@string/show_logs"'),
        ('android:text="Task Manager"', 'android:text="@string/task_manager"'),
        ('android:text="Memory"', 'android:text="@string/memory"'),
        ('android:text="Processes"', 'android:text="@string/processes"'),
        ('android:text="+ New Task"', 'android:text="@string/new_task_plus"'),
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
            print(f"  Note: {target} not in {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}: {replaced_count}/{len(pairs)} patterns replaced")

print("\nLocalization applied successfully!")
