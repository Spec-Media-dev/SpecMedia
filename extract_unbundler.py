import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'<script>\s*(document\.addEventListener.*?)</script>', content, re.DOTALL)
if m:
    js_code = m.group(1)
    print(f"Main unbundler JS length: {len(js_code)}")
    with open('unbundler.js', 'w', encoding='utf-8') as out:
        out.write(js_code)
    print("Written unbundler.js successfully")
else:
    print("Could not find main unbundler script!")
