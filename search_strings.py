import os

search_terms = [
    'Add games', 
    'Lock screen orientation', 
    'Vertical mode',
    'Horizontal mode',
    'Choose the Winlator theme', 
    'Overlay Opacity', 
    'Controls Editor',
    'No controllers connected',
    'Box64 Preset', 
    'FEXCore Preset',
    'Reinstall Imagefs',
    'Install SoundFont',
    'Winlator Path',
    'Shortcut Export Path',
    'Enable Big Picture Mode',
    'Set SteamGrid API Key',
    'Use DRI3 extension',
    'Capture External Pointer',
    'Disable Xinput',
    'Wine debug channels',
    'Search channels',
    'Enable File Provider',
    'Remove loading bar',
    'Downloadable Contents URL',
    'Balanced dark theme'
]

results = {}
for root, dirs, files in os.walk(r'a:\WorkSpace\sep 15,2026,winlator\ludashi_src'):
    for f in files:
        if f.endswith(('.xml', '.smali')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fl:
                    content = fl.read()
                    for term in search_terms:
                        if term in content:
                            if term not in results:
                                results[term] = []
                            results[term].append(path)
            except Exception as e:
                pass

for term, paths in results.items():
    print(f"=== Term: {term} ===")
    for p in paths[:5]:
        print(f"  {p}")
