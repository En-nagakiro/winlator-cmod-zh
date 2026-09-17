import os
import io
import shutil
import tarfile
import zstandard

base_assets = r'ludashi_src\assets'
font_file = 'wqy-microhei.ttc'

with open(font_file, 'rb') as f:
    font_data = f.read()

print(f"Loaded {font_file}: {len(font_data)} bytes")

# 1. Update container_pattern_common.tzst
common_path = os.path.join(base_assets, 'container_pattern_common.tzst')
print(f"Reading {common_path}...")
with open(common_path, 'rb') as fh:
    dctx = zstandard.ZstdDecompressor()
    decompressed = dctx.stream_reader(fh).read()

tar_in = tarfile.open(fileobj=io.BytesIO(decompressed), mode='r:*')
tar_out_buf = io.BytesIO()
tar_out = tarfile.open(fileobj=tar_out_buf, mode='w')

# Copy existing members except ones we might replace
fonts_to_add = {
    'home/xuser/.wine/drive_c/windows/Fonts/wqy-microhei.ttc': font_data,
    'home/xuser/.wine/drive_c/windows/Fonts/simsun.ttc': font_data,
    'home/xuser/.wine/drive_c/windows/Fonts/simsun.ttf': font_data,
    'home/xuser/.wine/drive_c/windows/Fonts/msyh.ttf': font_data,
}

existing_names = set()
for member in tar_in.getmembers():
    existing_names.add(member.name)
    if member.name in fonts_to_add:
        continue # will add fresh
    f = tar_in.extractfile(member) if member.isreg() else None
    tar_out.addfile(member, f)

# Add our fonts
for name, data in fonts_to_add.items():
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mode = 0o644
    info.mtime = 1726000000
    info.type = tarfile.REGTYPE
    tar_out.addfile(info, io.BytesIO(data))
    print(f"  Added font: {name} ({len(data)} bytes)")

tar_in.close()
tar_out.close()

# Compress back with zstd
cctx = zstandard.ZstdCompressor(level=15)
compressed_common = cctx.compress(tar_out_buf.getvalue())
with open(common_path, 'wb') as fh:
    fh.write(compressed_common)
print(f"Updated {common_path}: {len(compressed_common)} bytes")


# 2. Update proton-9.0-arm64ec_container_pattern.tzst & proton-9.0-x86_64_container_pattern.tzst
def patch_system_reg(content_str):
    content_str = content_str.replace('"MS Shell Dlg"="Tahoma"', '"MS Shell Dlg"="SimSun"')
    content_str = content_str.replace('"MS Shell Dlg 2"="Tahoma"', '"MS Shell Dlg 2"="Microsoft YaHei"')
    # 1) FontSubstitutes
    font_sub_sec = '[Software\\\\Microsoft\\\\Windows NT\\\\CurrentVersion\\\\FontSubstitutes]'
    substitutes_add = """
"MS Shell Dlg"="SimSun"
"MS Shell Dlg 2"="Microsoft YaHei"
"MS Sans Serif"="SimSun"
"Tahoma"="SimSun"
"Segoe UI"="Microsoft YaHei"
"System"="SimSun"
"SimSun"="SimSun"
"NSimSun"="NSimSun"
"Microsoft YaHei"="Microsoft YaHei"
"SimHei"="SimHei"
"宋体"="SimSun"
"新宋体"="NSimSun"
"微软雅黑"="Microsoft YaHei"
"黑体"="SimHei"
"楷体"="SimKai"
"""
    if font_sub_sec in content_str:
        idx = content_str.find(font_sub_sec)
        end_idx = content_str.find('\n', idx) # end of section header
        content_str = content_str[:end_idx] + substitutes_add + content_str[end_idx:]

    # 2) Fonts section
    fonts_sec = '[Software\\\\Microsoft\\\\Windows NT\\\\CurrentVersion\\\\Fonts]'
    fonts_add = """
"SimSun & NSimSun (TrueType)"="simsun.ttc"
"SimSun (TrueType)"="simsun.ttc"
"NSimSun (TrueType)"="simsun.ttc"
"Microsoft YaHei & Microsoft YaHei UI (TrueType)"="msyh.ttc"
"Microsoft YaHei (TrueType)"="msyh.ttc"
"WenQuanYi Micro Hei (TrueType)"="wqy-microhei.ttc"
"SimHei (TrueType)"="SimHei.ttf"
"Source Han Sans CN (TrueType)"="SourceHanSansCN-Regular.otf"
"""
    if fonts_sec in content_str:
        idx = content_str.find(fonts_sec)
        end_idx = content_str.find('\n', idx)
        content_str = content_str[:end_idx] + fonts_add + content_str[end_idx:]

    # 3) FontLink\SystemLink
    system_link_sec = """
[Software\\\\Microsoft\\\\Windows NT\\\\CurrentVersion\\\\FontLink\\\\SystemLink]
"Arial"=str(7):"simsun.ttc,SimSun\\0msyh.ttc\\0\\0"
"Courier New"=str(7):"simsun.ttc,SimSun\\0msyh.ttc\\0\\0"
"Lucida Sans Unicode"=str(7):"simsun.ttc,SimSun\\0msyh.ttc\\0\\0"
"Microsoft Sans Serif"=str(7):"simsun.ttc,SimSun\\0msyh.ttc\\0\\0"
"MS Sans Serif"=str(7):"simsun.ttc,SimSun\\0msyh.ttc\\0\\0"
"MS UI Gothic"=str(7):"simsun.ttc,SimSun\\0msyh.ttc\\0\\0"
"Segoe UI"=str(7):"msyh.ttc,Microsoft YaHei\\0simsun.ttc,SimSun\\0"
"Tahoma"=str(7):"simsun.ttc,SimSun\\0msyh.ttc\\0\\0"
"Times New Roman"=str(7):"simsun.ttc,SimSun\\0msyh.ttc\\0\\0"
"""
    content_str += system_link_sec
    return content_str

for pattern_file in ['proton-9.0-arm64ec_container_pattern.tzst', 'proton-9.0-x86_64_container_pattern.tzst']:
    pattern_path = os.path.join(base_assets, pattern_file)
    if not os.path.exists(pattern_path):
        continue
    print(f"Processing {pattern_file}...")
    with open(pattern_path, 'rb') as fh:
        dctx = zstandard.ZstdDecompressor()
        decompressed = dctx.stream_reader(fh).read()

    tar_in = tarfile.open(fileobj=io.BytesIO(decompressed), mode='r:*')
    tar_out_buf = io.BytesIO()
    tar_out = tarfile.open(fileobj=tar_out_buf, mode='w')

    for member in tar_in.getmembers():
        if member.name.endswith('system.reg'):
            f = tar_in.extractfile(member)
            reg_text = f.read().decode('utf-8', errors='ignore')
            patched_text = patch_system_reg(reg_text)
            new_data = patched_text.encode('utf-8')
            info = tarfile.TarInfo(name=member.name)
            info.size = len(new_data)
            info.mode = member.mode
            info.mtime = member.mtime
            info.type = tarfile.REGTYPE
            tar_out.addfile(info, io.BytesIO(new_data))
            print(f"  Patched system.reg: {len(reg_text)} -> {len(new_data)} bytes")
        else:
            f = tar_in.extractfile(member) if member.isreg() else None
            tar_out.addfile(member, f)

    tar_in.close()
    tar_out.close()

    cctx = zstandard.ZstdCompressor(level=15)
    compressed = cctx.compress(tar_out_buf.getvalue())
    with open(pattern_path, 'wb') as fh:
        fh.write(compressed)
    print(f"Updated {pattern_file}: {len(compressed)} bytes")

print("All container pattern assets successfully patched!")
