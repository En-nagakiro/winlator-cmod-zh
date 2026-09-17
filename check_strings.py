import zipfile, io, tarfile, zstandard

apk_path = 'Winlator_CMOD_Ludashi_zh_CN_Signed.apk'
z = zipfile.ZipFile(apk_path, 'r')
print('=== 1. Checking DEX files ===')
for f in z.namelist():
    if f.endswith('.dex'):
        print(' ', f, z.getinfo(f).file_size)

print('=== 2. Checking classes3.dex strings ===')
c3_data = z.read('classes3.dex')
check_terms = ['界面外观', '外部控制器', '按键透明度', '容器管理', '组件管理', '锁定屏幕方向', '竖屏模式', '横屏模式', '添加游戏']
for t in check_terms:
    print(f'  "{t}" present: {t.encode("utf-8") in c3_data}')

print('=== 3. Checking Assets container patterns ===')
dctx = zstandard.ZstdDecompressor()
common_data = z.read('assets/container_pattern_common.tzst')
dec = dctx.stream_reader(io.BytesIO(common_data)).read()
t = tarfile.open(fileobj=io.BytesIO(dec))
fonts = [m.name for m in t.getmembers() if any(k in m.name for k in ['wqy', 'simsun', 'msyh'])]
print('  Fonts in common.tzst:', fonts)

pat_data = z.read('assets/proton-9.0-arm64ec_container_pattern.tzst')
dec = dctx.stream_reader(io.BytesIO(pat_data)).read()
t = tarfile.open(fileobj=io.BytesIO(dec))
f = t.extractfile('.wine/system.reg')
txt = f.read().decode('utf-8', errors='ignore')
print('  MS Shell Dlg=SimSun in arm64ec:', '"MS Shell Dlg"="SimSun"' in txt)
print('  FontLink in arm64ec:', 'FontLink' in txt and 'SystemLink' in txt)

print('=== 4. Total files in APK ===', len(z.namelist()))
