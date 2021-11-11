import json
import glob

items = []

for file in glob.glob("./data/*.json"):
    with open(file, encoding='utf-8') as f:
        data = json.load(f)
    page_props = data['pageProps']
    if 'items' not in page_props:
        continue
    for item in page_props['items']:
        items.append(item)

with open('items.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=4)
