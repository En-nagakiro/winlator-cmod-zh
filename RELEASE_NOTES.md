# Release Notes / 发布说明

## `v11.2-cmod-a16-fix3` (2026-11-22)

**标题**：`Winlator CMOD 11.2 Fix 3 - Flyme/Android 16 反孤儿 Subreaper 根治、手柄修复与 Wine 开始菜单汉化`

### 核心变更

1. **反孤儿进程根治（替代 `ntdll.so` 硬编码补丁）**
   - 新增 368 字节纯静态 PIE（`ET_DYN`、64KB 对齐）AArch64 启动器 `lib/arm64-v8a/libsubreaper.so`，通过 `prctl(PR_SET_CHILD_SUBREAPER, 1)` 接管容器进程子树，并用 `wait4(-1)`（含 `-EINTR` 重试）回收已退出子进程。
   - 在 `ImageFs.find(Context)` 中初始化 `nativeLibraryDir`，在 `ProcessHelper.exec()` 中移除硬编码的 `patchNtdllIfNeeded()` 与 `prelaunchWineserverIfNeeded()`，统一用 `libsubreaper.so` 托管非 PulseAudio 的 Wine/Box64 启动。
   - **实测效果**：无需修改 `ntdll.so`，`wineserver`、`services.exe`、`winedevice.exe`、`plugplay.exe`、`rpcss.exe`、`explorer.exe` 全部保持存活且无僵尸进程；解除仅 `proton-9.0-arm64ec` 可进容器的限制，`proton-9.0-x86_64` 实测也可正常进入容器。

2. **手柄无响应问题修复**
   - 根因定位：早期版本中 `wineboot.exe` 初始化完成后退出，导致其子进程 `services.exe` 及 `winedevice.exe`（承载 `winebus.sys`、`winehid.sys`、`winexinput.sys`、`libSDL2`、`libfakeinput.so`）瞬间托孤给 PID 1 并被 Flyme 12.6 击杀，造成虚拟手柄与实体手柄均无法收到输入。接入 `libsubreaper.so` 后上述服务树持续存活。
   - 修正 `WineUtils.changeServicesStatus()` 中 `winebus:4`、`winehid:4` 为 `winebus:3`、`winehid:3`，并在 `XServerDisplayActivity` 中将配置标记升级为 `startupSelection_v4`，使旧容器（精简/正常模式）在下次启动时自动恢复手柄驱动服务。

3. **注册表与 Wine 开始菜单汉化补齐**
   - 修复 Compose 容器编辑器（`ContainerEditorV2Kt`、`ContainerSystemStorageInlineKt`）中误将 DirectInput 注册表键名 `"MouseWarpOverride"` 翻译成 `"鼠标抓取覆盖"` 的问题。
   - 同步中文版 `assets/wine_startmenu.json`（`程序`、`系统工具`、`我的电脑`、`任务管理器`、`注册表编辑器`、`命令提示符 (CMD)`、`Wine 配置 (Winecfg)` 等）。
   - 对内置 `proton-9.0-arm64ec` 与容器模板的 `explorer.exe`、`shell32.dll` 实施纯 PE `.rsrc` `RT_STRING` 显示字符串汉化（`开始`、`控制面板`、`Wine 控制面板`、`运行(&R)`、`退出桌面(&X)`、`桌面`、`我的电脑`、`Wine 资源管理器`、`位置:` 等），保留所有文件系统路径 ID（`Programs`、`Start Menu`、`Documents`、`StartUp` 等）不改动。

### 验证范围与说明
- **实测设备**：魅族 21 Note（骁龙 8 Gen 2 / Flyme 12.6 / Android 16 / 4KB 页）。
- **已验证**：`proton-9.0-arm64ec`（原版未修改 `ntdll.so`）与 `proton-9.0-x86_64` 进入容器；精简/激进模式下 `services.exe`/`winedevice.exe` 持续存活；虚拟手柄及 `event0` → `winexinput.sys` 事件通路；开始菜单中文显示。
- **未覆盖/已知边界**：实体蓝牙手柄与虚拟手柄共享同一条底层输入链路，本次打包校验未接物理蓝牙手柄单独实测；外部自行导入的第三方 Wine/Proton 包可享受 `libsubreaper.so` 进程保活，但其自带 `explorer.exe`/`shell32.dll` 仍为原版英文。
- **升级方式**：与 `fix` / `fix2` 签名一致，直接覆盖安装即可保留容器与数据。

### 安装包校验信息

| 文件名 | 大小 | MD5 | SHA-256 |
|---|---|---|---|
| `Winlator_CMOD_Ludashi_zh_CN_a16_fix3.apk` | `558.01 MB` (`585,120,110` 字节) | `3d649f1b5de9a75bb2ec8a7282b90dae` | `ad305be49513a7eef13ff92e2cd51c55e4721eb503d7eb4639cc89de68b96e7c` |

---

## 历史版本勘误说明

### `v11.2-cmod-a16-fix2` (2026-09-19，已被 `fix3` 替代)
- **实际包含的改动**：
  - 修复 `XServerDisplayActivity.getWineStartCommand()` 缺少 `winhandler.exe` 启动前缀导致的快捷方式启动黑屏；
  - 修复 `FileManagerFragment` 快捷方式路径映射，转为 Wine DOS 盘符路径（`D:\...`）；
  - 修复 `StringUtils.unescape()` 剥离反斜杠与 `FileUtils.getDirname()` 负索引越界崩溃。
- **已知问题**：沿用 `fix` 的硬编码 `ntdll.so` 方案，仅支持 `proton-9.0-arm64ec`，且在 Flyme 12.6 上存在 `services.exe`/`winedevice.exe` 被杀导致手柄失效的问题，建议直接升级至 `v11.2-cmod-a16-fix3`。

### `v11.2-cmod-a16-fix` (2026-09-17，已被 `fix3` 替代)
- **实际包含的改动**：
  - 在 `ProcessHelper` 中加入 `prelaunchWineserverIfNeeded()`（前台拉起 `wineserver -f -p`）与针对 `proton-9.0-arm64ec` `ntdll.so` 的原地双 fork 绕过补丁，首次在魅族 Flyme 12.6 上进入容器；
  - 调整 `WineUtils.changeServicesStatus()`（放行 `PlugPlay`/`RpcSs`）与 `Window.disableAllDescendants()`；
  - 完成主要 Android 界面中文化与容器模板中文字体（文泉驿微米黑 + `FontLink`）注入。
- **对原发布说明中不实信息的更正**：
  - 原说明声称修复了“16KB 页表 / Bionic FORTIFY `open64`/`fcntl64` 崩溃”以及“对 `explorer.exe` 实施 5 处指令级免疫补丁”——经二进制与真机复核，实测机型页大小为 4KB（`4096`），APK 中实际打包的 `wineserver` 与 `explorer.exe` 均未包含上述二进制补丁；真正使魅族进入容器的机制是上述 `ProcessHelper` 的反孤儿变通逻辑。
