import zstandard, tarfile, io

c = zstandard.ZstdDecompressor()
with open(r'apk_dex_smali\assets\container_pattern_common.tzst', 'rb') as f:
    d = c.decompress(f.read(), max_output_size=200*1024*1024)

with tarfile.open(fileobj=io.BytesIO(d)) as t:
    for m in t.getmembers():
        if m.name.endswith('system.reg'):
            data = t.extractfile(m).read().decode('utf-8', errors='ignore')
            for sec in data.split('['):
                if sec.startswith('System\\\\CurrentControlSet\\\\Services\\\\'):
                    name = sec.split(']')[0].split('\\\\')[-1]
                    if '"Start"=dword:00000002' in sec:
                        print('Auto (2):', name)
                    elif '"Start"=dword:00000003' in sec:
                        print('Demand (3):', name)
                    elif '"Start"=dword:00000004' in sec:
                        print('Disabled (4):', name)
