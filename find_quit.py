import urllib.request
import json

api_url = 'https://api.github.com/repos/wine-mirror/wine/contents/programs/explorer'
req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    for item in data:
        if item['name'].endswith(('.c', '.h')):
            raw_url = item['download_url']
            content = urllib.request.urlopen(raw_url).read().decode('utf-8', errors='replace')
            for i, line in enumerate(content.splitlines(), 1):
                if any(k in line for k in ['PostQuitMessage', 'WM_QUIT', 'WM_DESTROY', 'WM_CLOSE']):
                    print(f"{item['name']}:{i}: {line.strip()}")
except Exception as e:
    print('Error:', e)
