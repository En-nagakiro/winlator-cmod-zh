import os
import time
import zipfile
import hashlib

def file_info(path):
    if not os.path.exists(path):
        return "NOT FOUND"
    st = os.stat(path)
    mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))
    with open(path, 'rb') as f:
        data = f.read()
    h = hashlib.sha256(data).hexdigest()[:16]
    return f"size={st.st_size} mtime={mtime} sha256_prefix={h}"

print("ludashi_src/classes3.dex:", file_info(r'ludashi_src\classes3.dex'))
print("apk_dex_smali classes3.dex:", file_info(r'apk_dex_smali\build\apk\classes3.dex'))

z1 = zipfile.ZipFile(r'Winlator_CMOD_Ludashi_zh_CN_Signed.apk')
c3_apk = z1.read('classes3.dex')
print("Winlator_CMOD_Ludashi_zh_CN_Signed.apk classes3.dex:", len(c3_apk), hashlib.sha256(c3_apk).hexdigest()[:16])

z2 = zipfile.ZipFile(r'待汉化\winlator_wineserver_zh_CN_Signed.apk')
c3_zh = z2.read('classes3.dex')
print("待汉化/winlator_wineserver_zh_CN_Signed.apk classes3.dex:", len(c3_zh), hashlib.sha256(c3_zh).hexdigest()[:16])

z_orig = zipfile.ZipFile(r'待汉化\winlator_wineserver_unsigned.apk')
c3_orig = z_orig.read('classes3.dex')
print("待汉化/winlator_wineserver_unsigned.apk classes3.dex:", len(c3_orig), hashlib.sha256(c3_orig).hexdigest()[:16])
