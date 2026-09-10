import json, re, gzip, base64

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'<script type="__bundler/manifest">(.*?)</script>', content, re.DOTALL)
manifest = json.loads(m.group(1))

t = re.search(r'<script type="__bundler/template">(.*?)</script>', content, re.DOTALL)
template = json.loads(t.group(1))

ext = re.search(r'<script type="__bundler/ext_resources">(.*?)</script>', content, re.DOTALL)
ext_resources = json.loads(ext.group(1)) if ext else []

with open('unbundler.js', 'r', encoding='utf-8') as f:
    ujs = f.read()

# Extract the entire initSpecIntegration code from line 337 to 1060
start_marker = "// --- Spec Media Non-Intrusive Integration Layer ---"
end_marker = "}, 150);"

start_idx = ujs.find(start_marker)
end_idx = ujs.find(end_marker, start_idx) + len(end_marker)
integration_code = ujs[start_idx:end_idx]
print(f"Extracted integration code: {len(integration_code)} chars")

# Decode assets
asset_data_uris = {}
for uuid, entry in manifest.items():
    raw = base64.b64decode(entry['data'])
    if entry.get('compressed'):
        decomp = gzip.decompress(raw)
    else:
        decomp = raw
    mime = entry.get('mime', 'application/octet-stream')
    b64 = base64.b64encode(decomp).decode('ascii')
    asset_data_uris[uuid] = f"data:{mime};base64,{b64}"

# Replace UUIDs in template
page_html = template
for uuid, data_uri in asset_data_uris.items():
    page_html = page_html.replace(uuid, data_uri)

# Strip integrity/crossorigin
page_html = re.sub(r'\s+integrity="[^"]*"', '', page_html, flags=re.IGNORECASE)
page_html = re.sub(r'\s+crossorigin="[^"]*"', '', page_html, flags=re.IGNORECASE)

# Inject resource map
resource_map = {}
for entry in ext_resources:
    if entry['uuid'] in asset_data_uris:
        resource_map[entry['id']] = asset_data_uris[entry['uuid']]

resource_script = f'<script>window.__resources = {json.dumps(resource_map)};</script>'
head_match = re.search(r'<head[^>]*>', page_html, re.IGNORECASE)
if head_match:
    idx = head_match.end()
    page_html = page_html[:idx] + resource_script + page_html[idx:]

# Inject integration layer before </body>
integration_script = f"""
<script>
document.addEventListener('DOMContentLoaded', function() {{
  {integration_code}
}});
if (document.readyState === 'complete' || document.readyState === 'interactive') {{
  {integration_code}
}}
</script>
"""

body_idx = page_html.rfind('</body>')
if body_idx != -1:
    page_html = page_html[:body_idx] + integration_script + page_html[body_idx:]
else:
    page_html += integration_script

with open('clean_landing.html', 'w', encoding='utf-8') as f:
    f.write(page_html)

print(f"Saved clean_landing.html: {len(page_html)} characters")
