import struct

with open('C:/Users/86166/.gemini/antigravity/brain/364880ca-6f13-4915-aed3-aa01048bc456/explorer.exe', 'rb') as f:
    data = f.read()

# IAT mapping
pe_off = struct.unpack_from('<I', data, 0x3c)[0]
import_rva = struct.unpack_from('<I', data, pe_off + 136 + 8)[0]
off = import_rva
iat_map = {}
while off and off + 20 <= len(data):
    ilt, time, fwd, name_rva, iat = struct.unpack_from('<IIIII', data, off)
    if ilt == 0 and name_rva == 0: break
    dll_name = data[name_rva:data.find(b'\x00', name_rva)].decode()
    thunk_rva = iat
    ilt_rva = ilt if ilt else iat
    while True:
        entry = struct.unpack_from('<Q', data, ilt_rva)[0]
        if entry == 0: break
        if not (entry & 0x8000000000000000):
            fn_name = data[entry+2:data.find(b'\x00', entry+2)].decode()
            iat_map[thunk_rva] = f"{dll_name}!{fn_name}"
        ilt_rva += 8
        thunk_rva += 8
    off += 20

reg_page = {}
for off in range(0x2de0, 0x2ed0, 4):
    insn = struct.unpack_from('<I', data, off)[0]
    if (insn & 0x9f000000) == 0x90000000:
        rd = insn & 0x1f
        immlo = (insn >> 29) & 3
        immhi = (insn >> 5) & 0x7ffff
        imm = (immhi << 2) | immlo
        if imm & (1 << 20): imm -= (1 << 21)
        page = (off & ~0xfff) + (imm << 12)
        reg_page[rd] = page
        print(f"0x{off:x}: adrp x{rd}, 0x{page:x}")
    elif (insn & 0xffc00000) == 0xf9400000:
        rt = insn & 0x1f
        rn = (insn >> 5) & 0x1f
        imm12 = ((insn >> 10) & 0xfff) * 8
        addr = reg_page.get(rn, 0) + imm12
        comment = f" ; {iat_map.get(addr)}" if addr in iat_map else ""
        print(f"0x{off:x}: ldr x{rt}, [x{rn}, 0x{imm12:x}]{comment}")
    elif (insn & 0x7c000000) == 0x14000000:
        imm26 = insn & 0x3ffffff
        if imm26 & (1 << 25): imm26 -= (1 << 26)
        dest = off + (imm26 << 2)
        op = "bl" if (insn & 0x80000000) else "b"
        print(f"0x{off:x}: {op} 0x{dest:x}")
    elif (insn & 0xff000000) == 0x54000000:
        imm19 = (insn >> 5) & 0x7ffff
        if imm19 & (1 << 18): imm19 -= (1 << 19)
        dest = off + (imm19 << 2)
        print(f"0x{off:x}: b.cond 0x{dest:x}")
    elif (insn & 0x7e000000) == 0x34000000:
        is_cbnz = (insn & 0x01000000) != 0
        rt = insn & 0x1f
        imm19 = (insn >> 5) & 0x7ffff
        if imm19 & (1 << 18): imm19 -= (1 << 19)
        dest = off + (imm19 << 2)
        m = "cbnz" if is_cbnz else "cbz"
        print(f"0x{off:x}: {m} x{rt}, 0x{dest:x}")
    elif insn == 0xd63f0100:
        print(f"0x{off:x}: blr x8")
    elif (insn & 0xffffffe0) == 0xd61f0000:
        print(f"0x{off:x}: br x{insn & 0x1f}")
    else:
        print(f"0x{off:x}: 0x{insn:08x}")
