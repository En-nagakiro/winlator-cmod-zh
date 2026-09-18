# GitHub Release Notes / 发布说明

**建议版本标签 (Tag)**: `v11.2-cmod-a16-fix2`  
**建议发布标题 (Release Title)**: `Winlator CMOD 11.2 Fix 2 - Android 16 (16KB) & 游戏库快捷方式闪退修复 (深度自愈与全中文版)`

---

## 🇨🇳 中文说明 (Release Notes - Chinese)

### 🌟 核心亮点 (Highlights)
本版本重点解决了 **Android 16 预览版/正式版（包括魅族 Flyme 12.6 等系统）在骁龙 8 Gen 2 等新硬件平台上的闪退与黑屏问题**，并攻克了**从主界面游戏库快捷方式直接启动各类 Windows 游戏时的秒退与黑屏问题**，同时提供开箱即用的完整全中文界面与开箱即用的 3D 渲染环境。

- **全面兼容 Android 16 与 16KB 页表模式**：攻克 Bionic FORTIFY 安全检查导致的启动 `SIGABRT (Exit Code 134)` 闪退崩溃。
- **彻底根治“黑屏有声音”缺陷**：重构并修补 Wine 虚拟桌面宿主 `explorer.exe`，窗口关闭（点右上角 `[X]`、Alt+F4）或桌面刷新后画面常驻不灭，杜绝黑屏死锁。
- **彻底根治主界面游戏库快捷方式启动闪退**：重构 `StringUtils.unescape()` 保护 Windows DOS 路径反斜杠（防止 `D:\...` 损坏），并在 `FileUtils.getDirname()` 增加负索引边界安全检查，彻底消除 `StringIndexOutOfBoundsException`。
- **修复主界面快捷方式启动黑屏**：修复 `getWineStartCommand()` 补全 `winhandler.exe` 启动代理，并自动完成 DOS 盘符映射。
- **完整中文本地化 (zh-CN)**：主界面、容器管理、驱动切换、快捷方式与设置界面全部精细中文化。
- **开箱即用无须 ADB 补丁**：Patched 运行库已全部重构打包注入容器 Pattern，新建容器或全新安装均自动生效。

---

### 🛠️ 关键修复与技术细节 (Technical Improvements)

#### 1. 解决 Android 16 启动闪退 (SIGABRT Crash Fix)
- **底层根因**：Android 16 严格限制了 Bionic 的 FORTIFY 安全检查，并在 16KB 页表模式下对系统调用参数实施强校验。原生 `ntdll.so` 和 `wineserver` 在执行 `open64(O_CREAT)` 时缺少 `mode_t` 导致 libc 直接调用 `abort()`。
- **修复方案**：
  - 二进制 Patch `ntdll.so` 与 `wineserver` 中的 `__open64_chk` 和 `__fcntl64_chk`。
  - 保障 48-bit 虚拟地址空间兼容及 `mmap32` 内存预加载机制，保证在 Android 16 内核下平稳分配内存。

#### 2. 解决窗口关闭/刷新后黑屏有声音 (Black Screen Fix)
- **底层根因**：Wine 原生 `explorer.exe` 桌面处理函数 `desktop_wnd_proc` 存在原生退出机制：
  - 收到 `WM_SYSCOMMAND` + `SC_CLOSE` 时直接调用 `ExitWindowsEx(0, ~0)`；
  - 收到 `WM_CLOSE` 时调用 `PostQuitMessage(0)`，导致主消息循环 break 并调用 `ExitProcess(0)` 自杀退出；
  - 宿主退出导致嵌入式 X11 Server 丢失唯一的渲染窗口，画面变黑，但后台 `PulseAudio` 与 `wineserver` 依然运行。
- **修复方案**：
  - 对 ARM64 PE `explorer.exe` 实施 5 处指令级二进制免疫 Patch：
    1. 屏蔽 `SC_CLOSE` 调用的 `ExitWindowsEx`；
    2. 屏蔽 `WM_CLOSE` 调用的 `PostQuitMessage`；
    3. 消息循环拦截 `WM_QUIT` 并强制重新跳入 `GetMessageW`；
    4. 兜底切断所有可能落入 `ExitProcess` 的分支；
    5. 屏蔽托盘区销毁事件对进程生命周期的波及。

#### 3. 根治主界面快捷方式启动黑屏 (Shortcut Direct Launch Fix)
- **底层根因**：
  - `XServerDisplayActivity` 构建 Wine 快捷方式启动参数时漏掉了代理前缀 `winhandler.exe`，输出非法指令 `/dir <目录> "<文件>"`，导致 Wine `explorer.exe` 的 `CreateProcessW` 误将 `/dir` 当作程序名寻找 `/dir.exe` 失败退出，虚拟桌面全黑；
  - 内置文件管理器在“添加到游戏库”时，将 Linux 宿主绝对路径（`/storage/emulated/0/...`）硬编码写入 `.desktop`，缺少 Wine Windows 盘符上下文。
- **修复方案**：
  - 修复 `getWineStartCommand()`，正确装配 `winhandler.exe /dir` 启动守护命令；
  - 重构 `FileManagerFragment` 快捷方式写入逻辑，调用 `toDesktopWindowsPath` 自动将宿主路径映射转换为合法的容器 DOS 盘符路径（如 `D:\...`）。

#### 4. 根治游戏库快捷方式启动闪退 (Shortcut DOS Path & Negative Index Crash Fix)
- **底层根因**：
  - `Shortcut.java` 在解析 `.desktop` 文件中的 `Exec=... wine "D:\..."` 启动行时，调用 `StringUtils.unescape()`；
  - `StringUtils.unescape()` 误用正则表达式剥离了 Windows 路径中的所有反斜杠（如 `D:\Games\game.exe` 被洗成 `D:Gamesgame.exe`）；
  - `FileUtils.getDirname()` 因无任何斜杠返回 `-1`，随后调用 `path.substring(0, -1)` 触发 `StringIndexOutOfBoundsException` 导致主程序崩溃。
- **修复方案**：
  - 重写 `StringUtils.unescape()`，精确保留 Windows 路径反斜杠；
  - 在 `FileUtils.getDirname()` 中增加负索引边界安全防护，杜绝异常抛出。

---

### 📱 推荐配置与设备测试 (Tested Devices)
- **实测机型**：魅族 21 Note（Snapdragon 8 Gen 2 / Flyme 12.6 / Android 16）
- **推荐渲染设置**：
  - **图形驱动**：Turnip 26.2.0 (Adreno 7xx)
  - **DX 包装器**：DXVK 2.3.1 (ARM64EC GPLAsync)
  - **渲染模式**：Vulkan (Native)
  - **CPU 亲和性**：4-7 (性能核心)

---

### 📦 安装包校验信息 (Assets)

| 文件名 | 大小 | MD5 | SHA-256 |
|---|---|---|---|
| **`Winlator_CMOD_Ludashi_zh_CN_Final_Fixed.apk`** | 540.73 MB | `fdae5e5785058ae86c3fa712039dbb17` | `0469d20f336b8ec7ac45d542a278a254bc59dc0e9e1398d200658bf9521a8ed0` |

---


## 🌐 English Release Notes

### Highlights
- **Android 16 & 16KB Page Size Compatibility**: Fixed startup `SIGABRT` crash (Exit Code 134) caused by Bionic FORTIFY checks (`open64`/`fcntl64`).
- **Fixed Black Screen on Window Close/Refresh**: Eliminated the "black screen with audio still playing" bug by applying binary immunity patches to ARM64 `explorer.exe`.
- **Shortcut Direct Launch & Backslash Path Fix**: Fixed instant crash when launching games with Windows paths from Game Library due to regex backslash stripping in `StringUtils.unescape()` and unhandled negative index in `FileUtils.getDirname()`.
- **Full Chinese Localization**: Complete UI localization covering container management, settings, and input controls.
- **Built-in & Out-of-the-Box**: All patched runtime files (`ntdll.so`, `wineserver`, `explorer.exe`) are embedded into Proton 9.0 ARM64EC container patterns. No manual patching or ADB commands required!

### Technical Breakdown
1. **Startup Crash Fix**: Patched `open64` / `fcntl64` FORTIFY violations in `ntdll.so` and `wineserver`, ensuring reliable memory allocation under Android 16 16KB kernels and 48-bit mmap32 spaces.
2. **Desktop Lifecycle Immunity**: Patched `desktop_wnd_proc` and `manage_desktop` in `explorer.exe` to ignore `SC_CLOSE` and `WM_CLOSE`, redirect `WM_QUIT` back to the message loop, and prevent `ExitProcess(0)`.
3. **Shortcut Launch Crash Immunity**: Fixed path corruption in `StringUtils.unescape()` to preserve Windows path backslashes and added bounds checking in `FileUtils.getDirname()` to safely handle non-delimited strings without `StringIndexOutOfBoundsException`.

