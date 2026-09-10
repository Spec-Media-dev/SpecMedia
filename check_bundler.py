import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Total size of index.html: {len(content)} characters")

for tag in ['__bundler/manifest', '__bundler/template', '__bundler/page_order']:
    pattern = r'<script type="' + tag + r'">(.*?)</script>'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        data = m.group(1)
        print(f"Found {tag}, len={len(data)}")
        try:
            parsed = json.loads(data)
            print(f"  JSON parsed successfully! Keys/length: {len(parsed) if isinstance(parsed, (dict, list)) else 'scalar'}")
        except Exception as e:
            print(f"  JSON parse ERROR: {e}")
    else:
        print(f"MISSING {tag}!")
