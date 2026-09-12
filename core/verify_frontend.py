import urllib.request

urls = [
    ('http://127.0.0.1:8000/en/', 'en', 'ltr'),
    ('http://127.0.0.1:8000/ar/', 'ar', 'rtl'),
    ('http://127.0.0.1:8000/en/capabilities/', 'en', 'ltr'),
    ('http://127.0.0.1:8000/ar/capabilities/', 'ar', 'rtl'),
    ('http://127.0.0.1:8000/en/work/', 'en', 'ltr'),
    ('http://127.0.0.1:8000/ar/work/', 'ar', 'rtl'),
    ('http://127.0.0.1:8000/en/studio/', 'en', 'ltr'),
    ('http://127.0.0.1:8000/ar/studio/', 'ar', 'rtl'),
    ('http://127.0.0.1:8000/en/login/', 'en', 'ltr'),
    ('http://127.0.0.1:8000/ar/login/', 'ar', 'rtl'),
    ('http://127.0.0.1:8000/en/portal/', 'en', 'ltr'),
    ('http://127.0.0.1:8000/ar/portal/', 'ar', 'rtl'),
]

for url, lang, direction in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
        assert f'lang="{lang}"' in content, f'Missing lang={lang} in {url}'
        assert f'dir="{direction}"' in content, f'Missing dir={direction} in {url}'
        assert 'nav-lang-switcher' in content, f'Missing nav-lang-switcher in {url}'
        assert 'spec-landing-lang-bar' not in content, f'Found old floating lang bar in {url}'
        if lang == 'ar':
            assert 'Cairo' in content, f'Missing Cairo font in {url}'
        print(f'[PASS] {url} -> lang={lang}, dir={direction}, nav-lang-switcher=OK, floating=REMOVED')

print('\nALL 12 ENDPOINTS VERIFIED PERFECTLY!')
