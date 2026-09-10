import json, re, gzip, base64

# Read index.html to extract manifest, template, ext_resources
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'<script type="__bundler/manifest">(.*?)</script>', content, re.DOTALL)
manifest = json.loads(m.group(1))

t = re.search(r'<script type="__bundler/template">(.*?)</script>', content, re.DOTALL)
template = json.loads(t.group(1))

ext = re.search(r'<script type="__bundler/ext_resources">(.*?)</script>', content, re.DOTALL)
ext_resources = json.loads(ext.group(1)) if ext else []

print(f"Manifest keys: {len(manifest)}")
print(f"Template size: {len(template)}")

# Decode all assets into data URIs or inlined content
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
    print(f"Prepared {uuid}: mime={mime}, size={len(decomp)} bytes")

# Replace all uuid references in template with their data URIs
standalone_html = template
for uuid, data_uri in asset_data_uris.items():
    standalone_html = standalone_html.replace(uuid, data_uri)

# Strip any integrity or crossorigin attributes
standalone_html = re.sub(r'\s+integrity="[^"]*"', '', standalone_html, flags=re.IGNORECASE)
standalone_html = re.sub(r'\s+crossorigin="[^"]*"', '', standalone_html, flags=re.IGNORECASE)

# Inject resource map for any external resources
resource_map = {}
for entry in ext_resources:
    if entry['uuid'] in asset_data_uris:
        resource_map[entry['id']] = asset_data_uris[entry['uuid']]

resource_script = f'<script>window.__resources = {json.dumps(resource_map)};</script>'
head_match = re.search(r'<head[^>]*>', standalone_html, re.IGNORECASE)
if head_match:
    idx = head_match.end()
    standalone_html = standalone_html[:idx] + resource_script + standalone_html[idx:]

# Also check for the integration layer (scroll animation engine, contact form modal, footer rewire)
# Let's extract initSpecIntegration from unbundler.js and append it
with open('unbundler.js', 'r', encoding='utf-8') as f:
    ujs = f.read()

integration_match = re.search(r'(// --- Spec Media Non-Intrusive Integration Layer ---.*?)(?=\n\s*//\s*Resolve page-frame|\n\s*\}\s*catch|\Z)', ujs, re.DOTALL)
if integration_match:
    integration_code = integration_match.group(1)
    print("Found integration layer in unbundler.js, length:", len(integration_code))
    integration_tag = f"\n<script>\n{integration_code}\n</script>\n"
    body_close = standalone_html.rfind('</body>')
    if body_close != -1:
        standalone_html = standalone_html[:body_close] + integration_tag + standalone_html[body_close:]
    else:
        standalone_html += integration_tag

with open('standalone_test.html', 'w', encoding='utf-8') as f:
    f.write(standalone_html)

print(f"Generated standalone_test.html! Total size: {len(standalone_html)} characters")
