from django.test import TestCase, Client
from django.conf import settings
from django.utils.translation import activate, gettext as _


class LocalizationTestCase(TestCase):
    """
    Automated regression test suite for Spec Media internationalization (i18n),
    strictly localized to English (en) and Arabic (ar) with RTL layout integrity
    and navbar-integrated language switcher.
    """
    def setUp(self):
        self.client = Client()
        self.languages = ['en', 'ar']
        self.pages = [
            ('/', 'landing'),
            ('/capabilities/', 'capabilities'),
            ('/studio/', 'studio'),
            ('/work/', 'work'),
            ('/login/', 'login'),
            ('/404/', '404'),
        ]

    def test_root_redirects_to_default_language(self):
        """The bare root URL / must 302-redirect to /en/ by default."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get('Location'), '/en/')

    def test_unprefixed_endpoints_remain_accessible(self):
        """REST APIs and Technical SEO crawler files must NOT be prefixed by language codes."""
        health = self.client.get('/api/health/')
        self.assertEqual(health.status_code, 200)

        sitemap = self.client.get('/sitemap.xml')
        self.assertEqual(sitemap.status_code, 200)

        robots = self.client.get('/robots.txt')
        self.assertEqual(robots.status_code, 200)

    def test_set_language_redirects_with_proper_prefix(self):
        """The /set-language/ endpoint must switch between en and ar properly."""
        # Switch to Arabic
        res = self.client.get('/set-language/?lang=ar&next=/en/capabilities/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers.get('Location'), '/ar/capabilities/')
        self.assertIn(settings.LANGUAGE_COOKIE_NAME, res.cookies)
        self.assertEqual(res.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'ar')

        # Switch back to English
        res_en = self.client.get('/set-language/?lang=en&next=/ar/capabilities/')
        self.assertEqual(res_en.status_code, 302)
        self.assertEqual(res_en.headers.get('Location'), '/en/capabilities/')
        self.assertEqual(res_en.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'en')

        # Requesting removed language (e.g. French, German) must safely fall back to English
        res_fr = self.client.get('/set-language/?lang=fr&next=/ar/studio/')
        self.assertEqual(res_fr.status_code, 302)
        self.assertEqual(res_fr.headers.get('Location'), '/en/studio/')

    def test_all_pages_render_in_en_and_ar(self):
        """Every page route must render with correct lang and dir attributes in both English and Arabic."""
        for base_path, name in self.pages:
            for lang in self.languages:
                url = f'/{lang}/' if base_path == '/' else f'/{lang}{base_path}'
                expected_status = 404 if name == '404' else 200
                res = self.client.get(url)
                self.assertEqual(res.status_code, expected_status, f"Failed for {url}")

                content = res.content.decode('utf-8')
                self.assertIn(f'lang="{lang}"', content, f"Missing lang={lang} in {url}")

                if lang == 'ar':
                    self.assertIn('dir="rtl"', content, f"Missing dir=rtl in {url}")
                else:
                    self.assertIn('dir="ltr"', content, f"Missing dir=ltr in {url}")

                # Must have the navbar language switcher
                self.assertIn('nav-lang-switcher', content, f"Missing nav-lang-switcher in {url}")
                self.assertIn('EN', content, f"Missing EN in {url}")
                self.assertIn('العربية', content, f"Missing العربية in {url}")

    def test_only_english_and_arabic_configured(self):
        """Strictly English and Arabic must be configured, no other languages."""
        lang_codes = [code for code, name in settings.LANGUAGES]
        self.assertEqual(lang_codes, ['en', 'ar'])

    def test_portal_unauthenticated_redirects_with_lang_prefix(self):
        """Accessing protected portal route must preserve language code on login redirect."""
        res_en = self.client.get('/en/portal/')
        self.assertEqual(res_en.status_code, 302)
        self.assertEqual(res_en.headers.get('Location'), '/en/login/?next=/en/portal/')

        res_ar = self.client.get('/ar/portal/')
        self.assertEqual(res_ar.status_code, 302)
        self.assertEqual(res_ar.headers.get('Location'), '/ar/login/?next=/ar/portal/')

    def test_internal_navigation_links_preserve_arabic_prefix(self):
        """In Arabic views, navigation links should route with the /ar/ prefix."""
        res = self.client.get('/ar/capabilities/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertIn('href="/ar/work/"', content)
        self.assertIn('href="/ar/studio/"', content)
        self.assertIn('href="/ar/"', content)

    def test_localized_copy_presence(self):
        """Verify that translated strings actually appear in templates and gettext."""
        activate('ar')
        self.assertEqual(_("Four disciplines. One singular focus."), "أربعة تخصصات. تركيز واحد لا ينقسم.")

        activate('en')
        self.assertEqual(_("Four disciplines. One singular focus."), "Four disciplines. One singular focus.")
