import json, re, gzip, base64

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'<script type="__bundler/manifest">(.*?)</script>', content, re.DOTALL)
manifest = json.loads(m.group(1))

t = re.search(r'<script type="__bundler/template">(.*?)</script>', content, re.DOTALL)
template = json.loads(t.group(1))

ext = re.search(r'<script type="__bundler/ext_resources">(.*?)</script>', content, re.DOTALL)
ext_resources = json.loads(ext.group(1)) if ext else []

print(f"Total manifest entries: {len(manifest)}")
print(f"Template size: {len(template)} chars")
print(f"Ext resources: {ext_resources}")

for k, v in manifest.items():
    raw_data = base64.b64decode(v['data'])
    if v.get('compressed'):
        decomp = gzip.decompress(raw_data)
    else:
        decomp = raw_data
    mime = v.get("mime", "")
    print(f"UUID: {k} | mime: {mime} | comp: {v.get('compressed')} | size: {len(decomp)}")
    if 'javascript' in mime or 'text' in mime or 'json' in mime:
        print(f"   preview: {decomp[:120]}...")
    elif 'font' in mime:
        print(f"   font asset!")
    elif 'image' in mime:
        print(f"   image asset!")
