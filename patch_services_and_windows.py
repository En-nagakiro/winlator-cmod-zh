import os

def apply_patches():
    base_dir = r"a:\WorkSpace\sep 15,2026,winlator\apk_dex_smali"
    
    # 1. Patch WineUtils.smali
    wineutils_path = os.path.join(base_dir, r"smali_classes3\com\winlator\cmod\core\WineUtils.smali")
    with open(wineutils_path, "r", encoding="utf-8") as f:
        wu_content = f.read()
    
    old_wu_block1 = '    const-string v13, "PlugPlay:4"\n\n    const/4 v14, 0x5\n\n    aput-object v13, v2, v14\n\n    const-string v13, "RpcSs:4"'
    new_wu_block1 = '    const-string v13, "PlugPlay:2"\n\n    const/4 v14, 0x5\n\n    aput-object v13, v2, v14\n\n    const-string v13, "RpcSs:2"'
    assert old_wu_block1 in wu_content, "WineUtils block1 not found"
    wu_content = wu_content.replace(old_wu_block1, new_wu_block1, 1)

    old_wu_block2 = '    const-string v4, "PlugPlay:2"\n\n    aput-object v4, v1, v21\n\n    const/16 v4, 0xb\n\n    const-string v6, "RpcSs:3"'
    new_wu_block2 = '    const-string v4, "PlugPlay:2"\n\n    aput-object v4, v1, v21\n\n    const/16 v4, 0xb\n\n    const-string v6, "RpcSs:2"'
    assert old_wu_block2 in wu_content, "WineUtils block2 not found"
    wu_content = wu_content.replace(old_wu_block2, new_wu_block2, 1)

    old_wu_reg = '    invoke-virtual {v8, v3}, Lcom/winlator/cmod/core/WineRegistryEditor;->setCreateKeyIfNotExist(Z)V'
    new_wu_reg = '    invoke-virtual {v8, v5}, Lcom/winlator/cmod/core/WineRegistryEditor;->setCreateKeyIfNotExist(Z)V'
    assert old_wu_reg in wu_content, "WineUtils setCreateKeyIfNotExist not found"
    wu_content = wu_content.replace(old_wu_reg, new_wu_reg, 1)

    old_wu_block3 = '''    const-string v9, "PlugPlay"

    invoke-virtual {v10, v9}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v9

    if-eqz v9, :cond_1

    goto :goto_2'''
    new_wu_block3 = '''    const-string v9, "PlugPlay"

    invoke-virtual {v10, v9}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v9

    if-nez v9, :cond_2

    const-string v9, "RpcSs"

    invoke-virtual {v10, v9}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v9

    if-eqz v9, :cond_1

    goto :goto_2'''
    assert old_wu_block3 in wu_content, "WineUtils block3 not found"
    wu_content = wu_content.replace(old_wu_block3, new_wu_block3, 1)

    with open(wineutils_path, "w", encoding="utf-8") as f:
        f.write(wu_content)
    print("Patched WineUtils.smali successfully!")

    # 2. Patch XServerDisplayActivity.smali
    xs_path = os.path.join(base_dir, r"smali_classes3\com\winlator\cmod\XServerDisplayActivity.smali")
    with open(xs_path, "r", encoding="utf-8") as f:
        xs_content = f.read()

    old_xs_block = '''    .line 1052
    :goto_2
    iget-object v1, p0, Lcom/winlator/cmod/XServerDisplayActivity;->startupSelection:Ljava/lang/String;

    iget-object v4, p0, Lcom/winlator/cmod/XServerDisplayActivity;->container:Lcom/winlator/cmod/container/Container;

    invoke-virtual {v4, v2}, Lcom/winlator/cmod/container/Container;->getExtra(Ljava/lang/String;)Ljava/lang/String;'''
    new_xs_block = '''    .line 1052
    :goto_2
    const-string/jumbo v2, "startupSelection_v2"

    iget-object v1, p0, Lcom/winlator/cmod/XServerDisplayActivity;->startupSelection:Ljava/lang/String;

    iget-object v4, p0, Lcom/winlator/cmod/XServerDisplayActivity;->container:Lcom/winlator/cmod/container/Container;

    invoke-virtual {v4, v2}, Lcom/winlator/cmod/container/Container;->getExtra(Ljava/lang/String;)Ljava/lang/String;'''
    assert old_xs_block in xs_content, "XServerDisplayActivity block not found"
    xs_content = xs_content.replace(old_xs_block, new_xs_block, 1)

    with open(xs_path, "w", encoding="utf-8") as f:
        f.write(xs_content)
    print("Patched XServerDisplayActivity.smali successfully!")

    # 3. Patch Window.smali
    win_path = os.path.join(base_dir, r"smali_classes3\com\winlator\cmod\xserver\Window.smali")
    with open(win_path, "r", encoding="utf-8") as f:
        win_content = f.read()

    old_win_block = '''.method public disableAllDescendants()V
    .locals 4

    .line 410
    new-instance v0, Ljava/util/Stack;

    invoke-direct {v0}, Ljava/util/Stack;-><init>()V

    .line 411
    invoke-virtual {v0, p0}, Ljava/util/Stack;->push(Ljava/lang/Object;)Ljava/lang/Object;

    .line 412
    :goto_0
    invoke-virtual {v0}, Ljava/util/Stack;->isEmpty()Z

    move-result v1

    if-nez v1, :cond_0

    .line 413
    invoke-virtual {v0}, Ljava/util/Stack;->pop()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lcom/winlator/cmod/xserver/Window;

    .line 414
    iget-object v2, v1, Lcom/winlator/cmod/xserver/Window;->attributes:Lcom/winlator/cmod/xserver/WindowAttributes;

    const/4 v3, 0x0

    invoke-virtual {v2, v3}, Lcom/winlator/cmod/xserver/WindowAttributes;->setEnabled(Z)V

    .line 415
    iget-object v1, v1, Lcom/winlator/cmod/xserver/Window;->children:Ljava/util/ArrayList;

    invoke-virtual {v0, v1}, Ljava/util/Stack;->addAll(Ljava/util/Collection;)Z

    goto :goto_0

    :cond_0
    return-void
.end method'''

    new_win_block = '''.method public disableAllDescendants()V
    .locals 2

    .line 410
    iget-object v0, p0, Lcom/winlator/cmod/xserver/Window;->attributes:Lcom/winlator/cmod/xserver/WindowAttributes;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lcom/winlator/cmod/xserver/WindowAttributes;->setEnabled(Z)V

    return-void
.end method'''

    assert old_win_block in win_content, "Window.smali disableAllDescendants not found"
    win_content = win_content.replace(old_win_block, new_win_block, 1)

    with open(win_path, "w", encoding="utf-8") as f:
        f.write(win_content)
    print("Patched Window.smali successfully!")

if __name__ == "__main__":
    apply_patches()
