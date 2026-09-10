import json, re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

t = re.search(r'<script type="__bundler/template">(.*?)</script>', content, re.DOTALL)
template = json.loads(t.group(1))

for m in re.finditer(r'<script([^>]*)>', template):
    print("Script tag:", m.group(0))
