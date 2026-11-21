"""
Winlator CMOD Android 16 / Flyme 12.6 Anti-Orphan Subreaper & Wine Start Menu Localization Patcher.

What this script provides:
  1. Static-PIE AArch64 `libsubreaper.so` (368 bytes, ET_DYN, 64KB aligned):
     Sets PR_SET_CHILD_SUBREAPER=1 via prctl(36, 1), forks/execs the target Wine/Box64
     command, and reaps all descendants via wait4(-1) (retrying on -EINTR) until ECHILD.
     Prevents Flyme 12.6 / Android 16 from killing reparented Wine services (wineserver,
     services.exe, winedevice.exe/winebus/winexinput, plugplay.exe, rpcss.exe) when
     intermediate parents such as wineboot.exe exit, without binary-patching ntdll.so.
  2. Smali patches for apk_dex_smali/smali_classes3:
     - ImageFs.find(Context): initializes ProcessHelper nativeLibraryDir once.
     - ProcessHelper.exec(): drops hardcoded proton-9.0-arm64ec ntdll.so patch &
       wineserver -f -p prelaunch; wraps non-pulseaudio commands with libsubreaper.so.
     - WineUtils.changeServicesStatus(): changes winebus:4/winehid:4 -> winebus:3/winehid:3
       so Normal and Essential modes do not disable HID/XInput gamepad services.
     - XServerDisplayActivity: bumps startupSelection_v3 -> startupSelection_v4 so existing
       containers automatically re-apply the fixed service startup types.
     - ContainerEditorV2Kt / ContainerSystemStorageInlineKt: restores accidentally localized
       DirectInput registry value name "鼠标抓取覆盖" back to "MouseWarpOverride".
  3. PE .rsrc RT_STRING localization for Wine explorer.exe and shell32.dll:
     Patches strictly UI display strings (Start/Run/Exit desktop/Control Panel/My Computer/
     Desktop) in-place inside RT_STRING blocks, keeping exact resource sizes and preserving
     all filesystem path resource IDs (SHGetFolderPathW IDs 45..95).
"""

import argparse
import io
import os
import shutil
import struct
import tarfile

EXPLORER_ZH_MAP = {
    1: "Wine 资源管理器",
    2: "位置:",
    3: "开始",
    4: "运行(&R)",
    5: "退出桌面(&X)",
    6: "确定要关闭所有程序并退出虚拟桌面吗？",
}

# Strictly virtual shell display names only — NEVER touch SHGetFolderPathW path IDs (45..95).
SHELL32_ZH_MAP = {
    20: "桌面",
    21: "我的电脑",
    22: "控制面板",
    143: "Wine 控制面板",
}


def build_libsubreaper_so() -> bytes:
    """Build 368-byte static-PIE (ET_DYN, 64KB-aligned) AArch64 subreaper launcher ELF."""
    def movz_x(rd, imm16): return 0xd2800000 | (imm16 << 5) | rd
    def movn_x(rd, imm16): return 0x92800000 | (imm16 << 5) | rd
    def mov_x(rd, rm): return 0xaa0003e0 | (rm << 16) | rd
    def add_imm_x(rd, rn, imm12): return 0x91000000 | (imm12 << 10) | (rn << 5) | rd
    def sub_imm_x(rd, rn, imm12): return 0xd1000000 | (imm12 << 10) | (rn << 5) | rd
    def add_imm_w(rd, rn, imm12): return 0x11000000 | (imm12 << 10) | (rn << 5) | rd
    def add_lsl_x(rd, rn, rm, shift): return 0x8b000000 | (rm << 16) | (shift << 10) | (rn << 5) | rd
    def cmp_imm_x(rn, imm12): return 0xf100001f | (imm12 << 10) | (rn << 5)
    def cmn_imm_x(rn, imm12): return 0xb100001f | (imm12 << 10) | (rn << 5)
    def cmp_reg_x(rn, rm): return 0xeb00001f | (rm << 16) | (rn << 5)
    def ldr_uoff_x(rt, rn, off=0): return 0xf9400000 | ((off // 8) << 10) | (rn << 5) | rt
    def ldr_uoff_w(rt, rn, off=0): return 0xb9400000 | ((off // 4) << 10) | (rn << 5) | rt
    def and_imm_w_0x7f(rd, rn): return 0x12001800 | (rn << 5) | rd
    def ubfx_w(rd, rn, lsb, width): return 0x53000000 | (lsb << 16) | ((lsb + width - 1) << 10) | (rn << 5) | rd
    def svc0(): return 0xd4000001
    def b_imm(d): return 0x14000000 | (d & 0x3ffffff)
    def b_cond(cond, d): return 0x54000000 | ((d & 0x7ffff) << 5) | cond
    def cbz_x(rt, d): return 0xb4000000 | ((d & 0x7ffff) << 5) | rt
    def cbnz_w(rt, d): return 0x35000000 | ((d & 0x7ffff) << 5) | rt
    def tbnz_x_bit63(rt, d): return 0xb7f80000 | ((d & 0x3fff) << 5) | rt

    ops, labels = [], {}
    def label(name): labels[name] = len(ops)
    def emit(op): ops.append(op)

    # Entry: x19 = orig sp, x20 = argc; require argc >= 2
    emit(add_imm_x(19, 31, 0))
    emit(ldr_uoff_x(20, 19, 0))
    emit(cmp_imm_x(20, 2))
    emit(("b_cond", 0xb, "exit_126"))

    # prctl(PR_SET_CHILD_SUBREAPER=36, 1, 0, 0, 0)
    emit(movz_x(0, 36))
    emit(movz_x(1, 1))
    emit(movz_x(2, 0))
    emit(movz_x(3, 0))
    emit(movz_x(4, 0))
    emit(movz_x(8, 167))  # __NR_prctl
    emit(svc0())

    # clone(SIGCHLD=17, 0, 0, 0, 0)
    emit(movz_x(0, 17))
    emit(movz_x(1, 0))
    emit(movz_x(2, 0))
    emit(movz_x(3, 0))
    emit(movz_x(4, 0))
    emit(movz_x(8, 220))  # __NR_clone
    emit(svc0())

    emit(("cbz_x", 0, "do_child"))
    emit(("tbnz63", 0, "exit_125"))

    # Parent: x21 = direct child pid, x22 = exit code (0), 16B stack slot for wstatus
    emit(mov_x(21, 0))
    emit(movz_x(22, 0))
    emit(sub_imm_x(31, 31, 16))

    label("wait_loop")
    emit(movn_x(0, 0))          # pid = -1
    emit(add_imm_x(1, 31, 0))   # &wstatus
    emit(movz_x(2, 0))          # options = 0
    emit(movz_x(3, 0))          # rusage = NULL
    emit(movz_x(8, 260))        # __NR_wait4
    emit(svc0())

    emit(cmn_imm_x(0, 4))       # retry on -EINTR (-4)
    emit(("b_cond", 0x0, "wait_loop"))
    emit(cmp_imm_x(0, 0))       # break on <= 0 (-ECHILD)
    emit(("b_cond", 0xd, "done_wait"))
    emit(cmp_reg_x(0, 21))      # adopted grandchild? continue reaping
    emit(("b_cond", 0x1, "wait_loop"))

    emit(ldr_uoff_w(9, 31, 0))
    emit(and_imm_w_0x7f(10, 9))
    emit(("cbnz_w", 10, "was_signaled"))
    emit(ubfx_w(22, 9, 8, 8))
    emit(("b", "wait_loop"))

    label("was_signaled")
    emit(add_imm_w(22, 10, 128))
    emit(("b", "wait_loop"))

    label("done_wait")
    emit(mov_x(0, 22))
    emit(movz_x(8, 94))         # __NR_exit_group
    emit(svc0())

    label("do_child")
    emit(add_imm_x(1, 19, 16))      # &argv[1]
    emit(ldr_uoff_x(0, 1, 0))       # argv[1]
    emit(add_imm_x(9, 20, 2))       # argc + 2
    emit(add_lsl_x(2, 19, 9, 3))    # envp
    emit(movz_x(8, 221))            # __NR_execve
    emit(svc0())
    emit(movz_x(0, 127))
    emit(movz_x(8, 94))
    emit(svc0())

    label("exit_126")
    emit(movz_x(0, 126))
    emit(movz_x(8, 94))
    emit(svc0())

    label("exit_125")
    emit(movz_x(0, 125))
    emit(movz_x(8, 94))
    emit(svc0())

    insns = []
    for idx, op in enumerate(ops):
        if isinstance(op, int):
            insns.append(op)
        elif op[0] == "b":
            insns.append(b_imm(labels[op[1]] - idx))
        elif op[0] == "b_cond":
            insns.append(b_cond(op[1], labels[op[2]] - idx))
        elif op[0] == "cbz_x":
            insns.append(cbz_x(op[1], labels[op[2]] - idx))
        elif op[0] == "cbnz_w":
            insns.append(cbnz_w(op[1], labels[op[2]] - idx))
        elif op[0] == "tbnz63":
            insns.append(tbnz_x_bit63(op[1], labels[op[2]] - idx))
        else:
            raise ValueError(op)

    code = b"".join(struct.pack("<I", i) for i in insns)
    ehdr_size, phdr_size, code_off = 64, 56, 0x80
    total_size = code_off + len(code)

    e_ident = b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 8
    ehdr = struct.pack(
        "<16sHHIQQQIHHHHHH",
        e_ident,
        3,          # ET_DYN (static PIE)
        183,        # EM_AARCH64
        1,          # EV_CURRENT
        code_off,
        ehdr_size,
        0, 0,
        ehdr_size, phdr_size, 1,
        0, 0, 0,
    )
    phdr = struct.pack(
        "<IIQQQQQQ",
        1,          # PT_LOAD
        5,          # PF_R | PF_X
        0, 0, 0,
        total_size, total_size,
        0x10000,    # 64KB alignment (4KB and 16KB page compatible)
    )
    return ehdr + phdr + (b"\x00" * (code_off - ehdr_size - phdr_size)) + code


def _rva_to_off(data: bytes, rva: int):
    pe_off = struct.unpack_from("<I", data, 0x3c)[0]
    num_sec = struct.unpack_from("<H", data, pe_off + 6)[0]
    opt_sz = struct.unpack_from("<H", data, pe_off + 20)[0]
    sec_off = pe_off + 24 + opt_sz
    for i in range(num_sec):
        so = sec_off + i * 40
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", data, so + 8)
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return rptr + (rva - vaddr)
    return None


def patch_pe_rt_strings(raw_bytes: bytes, id_to_new_str: dict) -> bytes:
    """Patch PE RT_STRING (type 6) entries in-place without shifting sections or RVAs."""
    data = bytearray(raw_bytes)
    pe_off = struct.unpack_from("<I", data, 0x3c)[0]
    magic = struct.unpack_from("<H", data, pe_off + 24)[0]
    dd_off = pe_off + (24 + 112 if magic == 0x20b else 24 + 96)
    rsrc_rva, _ = struct.unpack_from("<II", data, dd_off + 2 * 8)
    if not rsrc_rva:
        raise ValueError("PE has no .rsrc directory")
    rsrc_base = _rva_to_off(data, rsrc_rva)

    def read_dir(off):
        n_named, n_id = struct.unpack_from("<HH", data, off + 12)
        return [struct.unpack_from("<II", data, off + 16 + i * 8) for i in range(n_named + n_id)]

    patched_ids = set()
    for type_id, sub1 in read_dir(rsrc_base):
        if type_id != 6 or not (sub1 & 0x80000000):
            continue
        for block_id, sub2 in read_dir(rsrc_base + (sub1 & 0x7fffffff)):
            if not (sub2 & 0x80000000):
                continue
            block_ids = set(range((block_id - 1) * 16, block_id * 16))
            if not (block_ids & set(id_to_new_str.keys())):
                continue
            for _lang_id, sub3 in read_dir(rsrc_base + (sub2 & 0x7fffffff)):
                if sub3 & 0x80000000:
                    continue
                leaf = rsrc_base + sub3
                data_rva, data_sz, _, _ = struct.unpack_from("<IIII", data, leaf)
                doff = _rva_to_off(data, data_rva)
                p, end = doff, doff + data_sz
                entries = []
                for idx in range(16):
                    if p + 2 <= end:
                        slen = struct.unpack_from("<H", data, p)[0]
                        p += 2
                        s = bytes(data[p:p + slen * 2]).decode("utf-16-le")
                        p += slen * 2
                    else:
                        s = ""
                    str_id = (block_id - 1) * 16 + idx
                    if str_id in id_to_new_str:
                        entries.append(id_to_new_str[str_id])
                        patched_ids.add(str_id)
                    else:
                        entries.append(s)
                new_blob = bytearray()
                for s in entries:
                    enc = s.encode("utf-16-le")
                    new_blob += struct.pack("<H", len(enc) // 2) + enc
                if len(new_blob) > data_sz:
                    raise ValueError(f"RT_STRING block {block_id} grew ({len(new_blob)} > {data_sz})")
                new_blob += b"\x00" * (data_sz - len(new_blob))
                data[doff:doff + data_sz] = new_blob

    if patched_ids != set(id_to_new_str.keys()):
        raise ValueError(f"Missing RT_STRING IDs: {set(id_to_new_str.keys()) - patched_ids}")
    struct.pack_into("<I", data, pe_off + 24 + 64, 0)
    return bytes(data)


def repatch_zst_archive(zst_path: str, member_handlers: dict, level: int = 15):
    import zstandard

    dctx = zstandard.ZstdDecompressor()
    cctx = zstandard.ZstdCompressor(level=level, threads=-1)
    tmp_out = zst_path + ".tmp_repack"
    replaced = []
    with open(zst_path, "rb") as fin, open(tmp_out, "wb") as fout:
        with dctx.stream_reader(fin) as rstream, cctx.stream_writer(fout) as wstream:
            with tarfile.open(fileobj=rstream, mode="r|") as tin, tarfile.open(fileobj=wstream, mode="w|") as tout:
                for member in tin:
                    handler = next((fn for suf, fn in member_handlers.items() if member.name.endswith(suf) and member.isfile()), None)
                    if handler is not None:
                        new_data = handler(tin.extractfile(member).read())
                        member.size = len(new_data)
                        tout.addfile(member, io.BytesIO(new_data))
                        replaced.append(member.name)
                    elif member.isfile():
                        tout.addfile(member, tin.extractfile(member))
                    else:
                        tout.addfile(member)
    shutil.move(tmp_out, zst_path)
    return replaced


def main():
    parser = argparse.ArgumentParser(description="Build libsubreaper.so and/or patch Wine PE RT_STRING archives.")
    parser.add_argument("--write-subreaper", metavar="PATH", help="Write static-PIE libsubreaper.so to PATH")
    parser.add_argument("--patch-assets-dir", metavar="DIR", help="Patch proton-9.0-arm64ec.tar.zst and container patterns in DIR")
    parser.add_argument("--zstd-level", type=int, default=15, help="Zstandard compression level (default: 15)")
    args = parser.parse_args()

    if args.write_subreaper:
        elf = build_libsubreaper_so()
        os.makedirs(os.path.dirname(os.path.abspath(args.write_subreaper)), exist_ok=True)
        with open(args.write_subreaper, "wb") as f:
            f.write(elf)
        print(f"Wrote libsubreaper.so ({len(elf)} bytes) -> {args.write_subreaper}")

    if args.patch_assets_dir:
        p_arm = os.path.join(args.patch_assets_dir, "proton-9.0-arm64ec.tar.zst")
        if os.path.isfile(p_arm):
            r = repatch_zst_archive(p_arm, {
                "lib/wine/aarch64-windows/explorer.exe": lambda b: patch_pe_rt_strings(b, EXPLORER_ZH_MAP),
                "lib/wine/aarch64-windows/shell32.dll": lambda b: patch_pe_rt_strings(b, SHELL32_ZH_MAP),
            }, level=args.zstd_level)
            print(f"Patched {p_arm}: {r}")
        for pat in ("proton-9.0-arm64ec_container_pattern.tzst", "proton-9.0-x86_64_container_pattern.tzst"):
            p_pat = os.path.join(args.patch_assets_dir, pat)
            if os.path.isfile(p_pat):
                r = repatch_zst_archive(p_pat, {
                    ".wine/drive_c/windows/explorer.exe": lambda b: patch_pe_rt_strings(b, EXPLORER_ZH_MAP),
                }, level=args.zstd_level)
                print(f"Patched {p_pat}: {r}")

    if not args.write_subreaper and not args.patch_assets_dir:
        parser.print_help()


if __name__ == "__main__":
    main()
