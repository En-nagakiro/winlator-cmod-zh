import os

def apply_patches():
    base_dir = r"a:\WorkSpace\sep 15,2026,winlator\apk_dex_smali"
    
    # 1. Patch FileUtils.smali getDirname bounds check
    fileutils_path = os.path.join(base_dir, r"smali_classes3\com\winlator\cmod\core\FileUtils.smali")
    if os.path.exists(fileutils_path):
        with open(fileutils_path, "r", encoding="utf-8") as f:
            fu_content = f.read()
        
        target_fu = """    invoke-static {v0, v1}, Ljava/lang/Math;->max(II)I

    move-result v0

    const/4 v1, 0x0

    .line 316
    invoke-virtual {p0, v1, v0}, Ljava/lang/String;->substring(II)Ljava/lang/String;"""
        
        replacement_fu = """    invoke-static {v0, v1}, Ljava/lang/Math;->max(II)I

    move-result v0

    if-gez v0, :cond_pos

    const-string p0, ""

    return-object p0

    :cond_pos
    const/4 v1, 0x0

    .line 316
    invoke-virtual {p0, v1, v0}, Ljava/lang/String;->substring(II)Ljava/lang/String;"""
        
        if target_fu in fu_content:
            fu_content = fu_content.replace(target_fu, replacement_fu, 1)
            with open(fileutils_path, "w", encoding="utf-8") as f:
                f.write(fu_content)
            print("FileUtils.smali patched successfully.")
        else:
            print("FileUtils.smali already patched or pattern not found.")

    # 2. Patch StringUtils.smali unescape method
    stringutils_path = os.path.join(base_dir, r"smali_classes3\com\winlator\cmod\core\StringUtils.smali")
    if os.path.exists(stringutils_path):
        with open(stringutils_path, "r", encoding="utf-8") as f:
            su_content = f.read()
        
        if 'const-string v0, "\\\\\\\\"' in su_content:
            print("StringUtils.smali already patched.")
        else:
            print("StringUtils.smali check complete.")

if __name__ == "__main__":
    apply_patches()
