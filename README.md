# Winlator CMOD Bionic 4.1 (魅族 Flyme / Android 16 兼容与中文版)

基于 Winlator CMOD Bionic 4.1（包名 `com.ludashi.benchmark`）进行反编译修补与中文化打包的维护版本。重点解决 **魅族 Flyme 12.6 / Android 16** 上容器无法启动、仅单一 Proton 版本可用、物理/虚拟手柄无响应，以及快捷方式路径闪退与中文化问题。

> **历史说明勘误**：早期 `v11.2-cmod-a16-fix` / `fix2` 的文档曾将魅族启动失败误归因于“Android 16 16KB 页表 / Bionic FORTIFY `open64`/`fcntl64`”，且误称已内置“5 处 `explorer.exe` 免疫补丁”。经后续真机 ADB 实测与二进制核验，测试机型魅族 21 Note 实际为标准 4KB 页（`PAGE_SIZE=4096`），`wineserver` 与 `explorer.exe` 均未包含上述补丁；真正的底层阻断原因是 **Flyme 12.6 对应用 UID 孤儿进程（`PPID=1`）的即时击杀机制**。当前版本文档与旧版 Release 说明已全部按实测证据修正。

---

## 核心改动 (What's Changed)

1. **Flyme 12.6 / Android 16 反孤儿进程根治（`libsubreaper.so`）**
   - 内置 368 字节纯静态 PIE（`ET_DYN`、64KB 对齐）AArch64 启动器 `lib/arm64-v8a/libsubreaper.so`，通过 `prctl(PR_SET_CHILD_SUBREAPER, 1)` 接管整个 Wine 进程子树，并通过 `wait4(-1)` 循环回收已退出子进程（支持 `-EINTR` 重试，兼容暂停/恢复）。
   - 移除早期版本中写死 `proton-9.0-arm64ec/lib/wine/aarch64-unix/ntdll.so` 路径与偏移的原地二进制魔改，以及 `wineserver -f -p` 预启动变通方案。
   - **实测效果**：无需修改 `ntdll.so`，`wineserver`、`services.exe`、`winedevice.exe`、`plugplay.exe`、`rpcss.exe`、`explorer.exe` 全部挂载在 `libsubreaper.so` 下持续存活、零僵尸进程；解除仅 `proton-9.0-arm64ec` 可进容器的限制，`proton-9.0-x86_64` 亦可正常进入容器。

2. **手柄服务与输入链路修复（虚拟手柄 / XInput）**
   - 解决了 `wineboot.exe` 退出后 `services.exe` / `winedevice.exe`（承载 `winebus.sys`、`winehid.sys`、`winexinput.sys`、`libSDL2`、`libfakeinput.so`）因托孤给 PID 1 被 Flyme 秒杀，导致虚拟手柄与实体手柄均无响应的问题。
   - 修正 `WineUtils.changeServicesStatus()`，将正常/精简启动模式下的 `winebus:4`、`winehid:4` 改为 `winebus:3`、`winehid:3`，并升级 `startupSelection_v4` 让旧容器启动时自动修复注册表。

3. **快捷方式启动与注册表修复**
   - 补全 `XServerDisplayActivity.getWineStartCommand()` 中的 `winhandler.exe` 启动前缀，修正 `FileManagerFragment` 快捷方式目标路径为 Wine DOS 盘符格式（`D:\...`）。
   - 修正 `StringUtils.unescape()` 误删 Windows 路径反斜杠的问题，并在 `FileUtils.getDirname()` 增加负索引防护，避免快捷方式启动崩溃。
   - 修正 `Window.disableAllDescendants()`，避免窗口切换/关闭后子窗口保持禁用状态。
   - 修正早期汉化误将注册表键名 `"MouseWarpOverride"` 翻成 `"鼠标抓取覆盖"` 的问题。

4. **中文界面、字体与 Wine 开始菜单本地化**
   - 覆盖 Android 主界面资源（`values-zh-rCN` / `values-zh`）及主要 Jetpack Compose 页面文案。
   - 在容器模板内置文泉驿微米黑字体（`wqy-microhei.ttc` 及 `SimSun`/`MSYH` 映射）与 `FontLink` 注册表配置。
   - 同步中文 `assets/wine_startmenu.json`，并对内置 `proton-9.0-arm64ec` 与容器模板中的 `explorer.exe`、`shell32.dll` 实施纯 PE `.rsrc` `RT_STRING` 显示字符串汉化（`开始`、`控制面板`、`运行(&R)`、`退出桌面(&X)`、`桌面`、`我的电脑`、`Wine 资源管理器` 等），严格保留所有文件系统路径资源 ID（`Programs`、`Start Menu`、`Documents`、`StartUp` 等）。

---

## 技术原理简述

### 为什么魅族 Flyme 12.6 进不去容器且手柄失灵？
在魅族 21 Note（Flyme 12.6 / Android 16）上进行的控制变量测试表明：
- `adb shell`（`uid=2000`）下的双 fork 孤儿进程（`PPID=1`）正常存活；
- 普通应用 UID（如 `u0_a346`）下的直接子进程正常存活，但只要中间父进程退出、子进程托孤给 `init`（`PPID=1`），会在 `< 100ms` 内被系统静默终止。

早期版本仅通过原地 patch `proton-9.0-arm64ec` 的 `ntdll.so` 跳过创建时的二次 `fork()`，使 `services.exe` 暂时成为 `wineboot.exe` 的直接子进程；但启动约 0.2 秒后 `wineboot.exe` 正常退出，`services.exe` 与其子树 `winedevice.exe`（负责读取 `dev/input/event0` 并提供 HID/XInput 驱动）仍会变成孤儿被瞬间击杀，同时导致所有未打补丁的其他 Wine/Proton 版本无法启动。

引入 `libsubreaper.so` 设置 `PR_SET_CHILD_SUBREAPER` 后，所有失去直接父进程的 Wine 子进程均由内核重挂到存活的 `libsubreaper.so` 下（不再进入 PID 1），从根源上同时解决了多版本启动、手柄服务存活与僵尸进程回收三个问题。相关构造与补丁逻辑见 [patch_subreaper_and_wine_zh.py](patch_subreaper_and_wine_zh.py)。

---

## 安装与使用说明

1. 前往 [Releases](../../releases) 下载最新的 `Winlator_CMOD_Ludashi_zh_CN_a16_fix3.apk`。
2. 本包沿用 `uber-apk-signer` 内置调试签名，与 `fix` / `fix2` 签名一致，可直接覆盖安装并保留现有容器与数据。
3. 如之前手动开启过“设置 → Wine 调试”，确认正常后建议关闭以减少日志开销。

### 已实测范围与已知限制
- **已真机验证**：魅族 21 Note（骁龙 8 Gen 2 / Flyme 12.6 / Android 16 / 4KB 页）：
  - 原版未修改 `ntdll.so` 正常进入 `proton-9.0-arm64ec` 与 `proton-9.0-x86_64` 容器；
  - `services.exe` / `winedevice.exe` / `plugplay.exe` / `rpcss.exe` 持续存活且零僵尸；
  - 虚拟手柄及 `event0` → `libfakeinput.so` → `SDL2` → `winebus`/`winexinput` 通路工作正常；
  - Wine 开始菜单中文项显示正常。
- **已知边界**：
  - 实体蓝牙手柄与虚拟手柄共享上述底层链路，打包验证阶段未接实体蓝牙手柄单独复测，建议自行连机确认；
  - 从外部单独导入的第三方 Wine/Proton 包可自动受益于 `libsubreaper.so` 反孤儿保护，但其自带的 `explorer.exe`/`shell32.dll` 仍保持原版英文。

---

## 最新安装包校验信息 (`v11.2-cmod-a16-fix3`)

| 项目 | 值 |
|---|---|
| 文件名 | `Winlator_CMOD_Ludashi_zh_CN_a16_fix3.apk` |
| 大小 | `558.01 MB` (`585,120,110` 字节) |
| MD5 | `3d649f1b5de9a75bb2ec8a7282b90dae` |
| SHA-256 | `ad305be49513a7eef13ff92e2cd51c55e4721eb503d7eb4639cc89de68b96e7c` |
