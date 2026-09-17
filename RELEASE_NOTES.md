# GitHub Release Notes / 发布说明

**建议版本标签 (Tag)**: `v11.2-cmod-a16-fix`  
**建议发布标题 (Release Title)**: `Winlator CMOD 11.2 - Android 16 (16KB) & Black Screen Fix (深度自愈与全中文版)`

---

## 🇨🇳 中文说明 (Release Notes - Chinese)

### 🌟 核心亮点 (Highlights)
本版本重点解决了 **Android 16 预览版/正式版（包括魅族 Flyme 12.6 等系统）在骁龙 8 Gen 2 等新硬件平台上的闪退与黑屏问题**，同时提供开箱即用的完整全中文界面与开箱即用的 3D 渲染环境。

- **全面兼容 Android 16 与 16KB 页表模式**：攻克 Bionic FORTIFY 安全检查导致的启动 `SIGABRT (Exit Code 134)` 闪退崩溃。
- **彻底根治“黑屏有声音”缺陷**：重构并修补 Wine 虚拟桌面宿主 `explorer.exe`，窗口关闭（点右上角 `[X]`、Alt+F4）或桌面刷新后画面常驻不灭，杜绝黑屏死锁。
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
| **`Winlator_CMOD_Ludashi_zh_CN_Final_Fixed.apk`** | 540.75 MB | `79d5662d5154b32b58b915d581a454fe` | `3b226debb212a47639f11c7652fb02ac975266436a8f3d443ec9a10fcfa66b06` |

---

## 🌐 English Release Notes

### Highlights
- **Android 16 & 16KB Page Size Compatibility**: Fixed startup `SIGABRT` crash (Exit Code 134) caused by Bionic FORTIFY checks (`open64`/`fcntl64`).
- **Fixed Black Screen on Window Close/Refresh**: Eliminated the "black screen with audio still playing" bug by applying binary immunity patches to ARM64 `explorer.exe`.
- **Full Chinese Localization**: Complete UI localization covering container management, settings, and input controls.
- **Built-in & Out-of-the-Box**: All patched runtime files (`ntdll.so`, `wineserver`, `explorer.exe`) are embedded into Proton 9.0 ARM64EC container patterns. No manual patching or ADB commands required!

### Technical Breakdown
1. **Startup Crash Fix**: Patched `open64` / `fcntl64` FORTIFY violations in `ntdll.so` and `wineserver`, ensuring reliable memory allocation under Android 16 16KB kernels and 48-bit mmap32 spaces.
2. **Desktop Lifecycle Immunity**: Patched `desktop_wnd_proc` and `manage_desktop` in `explorer.exe` to ignore `SC_CLOSE` and `WM_CLOSE`, redirect `WM_QUIT` back to the message loop, and prevent `ExitProcess(0)`.
