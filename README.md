# Winlator CMOD (Android 16 & 16KB Compatible / 完整中文定制版)

[![Android 16 Supported](https://img.shields.io/badge/Android-16%20Ready-green.svg)](https://developer.android.com/about/versions/16)
[![16KB Page Compatible](https://img.shields.io/badge/Page%20Size-16KB%20Compatible-blue.svg)](https://developer.android.com/guide/practices/page-sizes)
[![License](https://img.shields.io/badge/License-GPL%20v3-orange.svg)](LICENSE)

基于 Winlator CMOD 进行深度系统级强化与全中文化的定制版本。完美解决 **Android 16 预览版/正式版（如魅族 Flyme 12.6 等系统）+ 骁龙 8 Gen 2 / 8 Gen 3** 等新硬件上的闪退崩溃，并彻底攻克 Wine 虚拟桌面“关闭窗口/刷新后黑屏有声音”的历史级疑难问题。

---

## 🌟 核心特性 (Key Features)

1. **Android 16 & 16KB 页表原生兼容**
   - 彻底解决由于 Android 16 Bionic FORTIFY 严格参数校验（`open64`/`fcntl64`）导致的 `SIGABRT` (Exit Code 134) 启动崩溃。
   - 原生支持 16KB 内存页对齐与 48 位虚拟地址空间 `mmap32` 内存分配隔离。

2. **虚拟桌面防自杀免疫修补 (Immunity Patch)**
   - 攻克 Windows 窗口关闭（点击 `[X]`、Alt+F4）或右键刷新桌面时触发宿主退出的漏洞。
   - 虚拟桌面宿主 `explorer.exe` 常驻不灭，杜绝“前台黑屏、后台音频继续播放”的失步死锁。

3. **开箱即用 (Out-of-the-Box Ready)**
   - 修复补丁均已内建并预编译至 Proton 9.0 ARM64EC 容器包与模板中，新建容器自动生效，无需任何 ADB 命令行修补。

4. **精致全中文界面 (zh-CN Localization)**
   - 容器配置、驱动切换、快捷方式管理、预设模式及侧边栏设置实现 100% 精准中文化。

---

## 🚀 快速上手 (Getting Started)

### 1. 安装与权限
1. 前往 [Releases](../../releases) 下载最新的 `Winlator_CMOD_Ludashi_zh_CN_Final_Fixed.apk`。
2. 安装并启动，授予常规存储与管理权限。

### 2. 推荐容器参数 (以骁龙 8 Gen 2 为例)
- **Wine 版本**：`Proton 9.0 (ARM64EC)`
- **显卡驱动 (GPU Driver)**：`Turnip 26.2.0 (Adreno 7xx)`
- **DX 包装器**：`DXVK 2.3.1 (ARM64EC GPLAsync)`
- **渲染器**：`Vulkan (Native)`
- **音频驱动**：`PulseAudio`
- **CPU 亲和性**：勾选核心 `4, 5, 6, 7`

---

## 🔧 技术原理解析 (Under the Hood)

### 1. FORTIFY open64/fcntl64 Bionic Crash
Android 16 强化了 libc 运行期安全检查。若 `open64()` 携带 `O_CREAT` 但未传入合法的 `mode_t`，或者 `fcntl64()` 传参异常，Android 16 libc 会直接调用 `abort()`。本项目在二进制层对 `ntdll.so` 及 `wineserver` 进行了指令修正与符号包裹，杜绝崩溃触发。

### 2. Desktop Lifecycle & Black Screen Fix
Wine 原生 `desktop_wnd_proc` 在收到 `WM_SYSCOMMAND` (`SC_CLOSE`) 时会调用 `ExitWindowsEx(0, ~0)`，收到 `WM_CLOSE` 时调用 `PostQuitMessage(0)`，导致 `manage_desktop` 退出消息循环并执行 `ExitProcess(0)`。
本项目对 ARM64 PE `explorer.exe` 实施了 5 处指令级二进制免疫补丁：
- 拦截 `SC_CLOSE` 与 `WM_CLOSE`，直接返回 0；
- 消息循环强制屏蔽 `WM_QUIT`，退出分支兜底跳转回主循环，保障 X11 桌面窗口永驻。

---

## 📜 校验信息 (Binary Checksum)

- **文件**: `Winlator_CMOD_Ludashi_zh_CN_Final_Fixed.apk`
- **大小**: `540.75 MB (567,015,715 字节)`
- **MD5**: `79d5662d5154b32b58b915d581a454fe`
- **SHA256**: `3b226debb212a47639f11c7652fb02ac975266436a8f3d443ec9a10fcfa66b06`
