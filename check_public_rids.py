import re

res_ids = {
    '0x7f1002a7': 'sound?',
    '0x7f10030f': 'xserver?',
    '0x7f10015c': 'logs?',
    '0x7f1000eb': 'experimental?',
    '0x7f100134': 'imagefs?'
}

with open(r'ludashi_src\res\values\public.xml', 'r', encoding='utf-8') as f:
    for line in f:
        for rid in res_ids:
            if f'id="{rid}"' in line:
                print(f"{rid} -> {line.strip()}")
