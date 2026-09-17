import zipfile
import sys

apk_path = 'Winlator_CMOD_Ludashi_zh_CN_Signed.apk'
z = zipfile.ZipFile(apk_path)

dex_files = [f for f in z.namelist() if f.endswith('.dex')]
print(f"DEX files in APK: {dex_files}")

dex_data = {f: z.read(f) for f in dex_files}

terms_to_check = [
    # Screenshot 1 & 2
    ('Library', ['游戏库']),
    ('Favorites', ['收藏']),
    ('Recent', ['最近']),
    ('Add games', ['添加游戏']),
    ('Lock screen orientation', ['锁定屏幕方向']),
    ('Vertical mode', ['竖屏模式']),
    ('Horizontal mode', ['横屏模式']),
    # Screenshot 3
    ('Profile', ['配置方案', '预设方案']),
    ('-- Select Profile --', ['-- 选择配置方案 --', '-- 选择预设方案 --']),
    ('Overlay Opacity', ['按键透明度', '遮罩透明度']),
    ('Import', ['导入']),
    ('Export', ['导出']),
    ('Controls Editor', ['按键编辑器']),
    ('EXTERNAL CONTROLLERS', ['外部控制器']),
    ('No controllers connected', ['未连接控制器', '未连接外部控制器']),
    # Screenshot 4
    ('APPEARANCE', ['界面外观']),
    ('Theme', ['主题', '界面主题']),
    ('Containers', ['容器', '容器管理']),
    ('Create and manage Windows environments', ['创建和管理 Windows 运行环境', '创建和管理 Windows 环境']),
    ('Appearance', ['界面外观', '主题外观']),
    ('Choose the Winlator theme. Changes are applied immediately.', ['选择 Winlator 主题', '更改将立即生效']),
    ('Bright surfaces with dark text', ['浅色', '深色文本', '明亮']),
    ('Balanced dark theme', ['深色主题', '平衡']),
    ('Pure black background for OLED displays', ['纯黑', 'OLED']),
    ('Dark interface with cool blue accents', ['暗色界面', '蓝']),
    ('Dark interface with warm red accents', ['暗色界面', '红']),
    ('Dark interface with rich purple accents', ['暗色界面', '紫']),
    # Screenshot 5
    ('Components', ['组件', '组件管理']),
    ('Wine, Proton, DXVK, VKD3D and runtimes', ['Wine、Proton、DXVK、VKD3D 及运行库组件', 'Wine, Proton, DXVK, VKD3D']),
    ('PRESETS', ['预设', '预设配置']),
    ('Box64 Preset', ['Box64 预设']),
    ('FEXCore Preset', ['FEXCore 预设']),
    ('Stability', ['稳定性']),
    ('Compatibility', ['兼容性']),
    ('Intermediate', ['均衡模式', '中等', '平衡']),
    ('Performance', ['高性能', '性能']),
    # Screenshot 6 & 7
    ('SOUND', ['声音', '声音设置', '音频']),
    ('Install SoundFont', ['安装 SoundFont 音色库', '安装 SoundFont']),
    ('PATH SETTINGS', ['路径设置']),
    ('Winlator Path', ['Winlator 根路径', 'Winlator 路径']),
    ('Shortcut Export Path', ['快捷方式导出路径']),
    ('BIG PICTURE MODE', ['大屏模式']),
    ('Enable Big Picture Mode on App Launch', ['启动应用时开启大屏模式', '大屏模式']),
    ('Set SteamGrid API Key? (Cover Art)', ['设置 SteamGrid API 密钥', 'SteamGrid']),
    ('XSERVER', ['X 服务器', 'XSERVER']),
    ('Cursor speed', ['光标移动速度', '光标速度']),
    ('Use DRI3 extension', ['使用 DRI3 扩展', 'DRI3']),
    ('Capture External Pointer', ['捕获外部鼠标指针', '捕获外部指针']),
    ('Disable Xinput (Used for Exclusive M/KB support)', ['禁用 XInput (用于独占键鼠支持)', '禁用 XInput']),
    ('LOGS', ['日志', '日志设置']),
    ('Enable Wine debug', ['开启 Wine 调试日志', '启用 Wine 调试']),
    ('Wine debug channels', ['Wine 调试通道']),
    ('Enable Box64 logs', ['开启 Box64 日志', '启用 Box64 日志']),
    ('EXPERIMENTAL', ['实验性功能', '实验性选项']),
    ('Enable File Provider', ['启用文件提供器', '文件提供器']),
    ('Open Android Browser in Wine', ['在 Wine 中调用安卓浏览器', '安卓浏览器']),
    ('Share Android Clipboard with Wine', ['与 Wine 共享安卓剪贴板', '安卓剪贴板']),
    ('Suspend Wine when app is in background', ['应用进入后台时挂起 Wine', '后台挂起']),
    ('Enable High Refresh Rate Mode', ['启用高刷新率模式', '高刷新率']),
    # Screenshot 8 & 9
    ('Search channels', ['搜索调试通道', '搜索通道']),
    ('Remove loading bar when booting games', ['启动游戏时移除加载条', '移除加载条']),
    ('Downloadable Contents URL', ['可下载资源 URL 地址', 'DLC 下载链接', '可下载内容']),
    ('IMAGEFS', ['系统镜像', 'IMAGEFS', '系统映像']),
    ('Reinstall Imagefs', ['重新安装系统镜像', '重新安装系统映像']),
    ('About', ['关于 Winlator', '关于', '关于与版本信息'])
]

print("\n--- CHECKING TERMS IN APK ---")
for en, zh_options in terms_to_check:
    en_in = [dex_name for dex_name, data in dex_data.items() if en.encode('utf-8') in data]
    zh_found = []
    for zh in zh_options:
        for dex_name, data in dex_data.items():
            if zh.encode('utf-8') in data:
                zh_found.append((zh, dex_name))
    
    status = "OK"
    if en_in:
        if zh_found:
            status = f"BOTH (EN in {en_in}, ZH: {zh_found[0][0]})"
        else:
            status = f"MISSING TRANSLATION (EN in {en_in})"
    else:
        if zh_found:
            status = f"FULLY TRANSLATED ({zh_found[0][0]} in {zh_found[0][1]})"
        else:
            status = "NEITHER FOUND IN DEX (maybe in resources.arsc?)"
    print(f"[{status}] {en}")
