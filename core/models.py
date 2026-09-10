from django.db import models

class SEOPage(models.Model):
    """
    Stores canonical SEO metadata and Schema.org structured data
    for every indexable and public route on Spec Media.
    """
    SCHEMA_CHOICES = [
        ('Organization', 'Organization'),
        ('Service', 'Service'),
        ('WebPage', 'WebPage'),
        ('CollectionPage', 'CollectionPage'),
        ('ContactPage', 'ContactPage'),
        ('AboutPage', 'AboutPage'),
    ]

    route_path = models.CharField(max_length=255, unique=True, help_text="Canonical URL path, e.g. / or /services/seo-agency-dubai/")
    page_name = models.CharField(max_length=150, help_text="Human-readable title in the CMS")
    meta_title = models.CharField(max_length=255, help_text="Browser <title> and Google search snippet title")
    meta_description = models.TextField(blank=True, help_text="Search engine meta description (150-160 chars)")
    canonical_url = models.CharField(max_length=500, blank=True, help_text="Full canonical URL (e.g. https://www.spec-media.com/...)")
    primary_keyword = models.CharField(max_length=150, blank=True, help_text="Primary commercial search term")
    secondary_keywords = models.TextField(blank=True, help_text="Comma-separated secondary keywords")
    og_title = models.CharField(max_length=255, blank=True, help_text="Open Graph title for social sharing")
    og_description = models.TextField(blank=True, help_text="Open Graph description")
    og_image_url = models.CharField(max_length=500, blank=True, help_text="Social preview image URL")
    schema_type = models.CharField(max_length=50, default='Service', choices=SCHEMA_CHOICES)
    is_indexable = models.BooleanField(default=True, help_text="Whether search engines should index this route")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Page"
        verbose_name_plural = "SEO Pages"
        ordering = ['route_path']

    def __str__(self):
        return f"{self.route_path} — {self.meta_title}"


class WorkProject(models.Model):
    """
    Stores portfolio case studies and proof entities that validate
    Spec Media services, industries, and measurable commercial results.
    """
    DISCIPLINE_CHOICES = [
        ('SEO & Organic Growth', 'SEO & Organic Growth'),
        ('Web & Experience Systems', 'Web & Experience Systems'),
        ('AI Marketing & Automation', 'AI Marketing & Automation'),
        ('Brand Architecture & Design', 'Brand Architecture & Design'),
        ('Paid Performance Media', 'Paid Performance Media'),
        ('Content & Motion Production', 'Content & Motion Production'),
    ]

    MARKET_CHOICES = [
        ('Dubai', 'Dubai'),
        ('UAE', 'UAE'),
        ('MENA', 'MENA'),
        ('Global', 'Global'),
    ]

    title = models.CharField(max_length=200, help_text="Project / Case Study title")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL slug (e.g. aether-hyperion-dubai)")
    client = models.CharField(max_length=150, help_text="Client brand or sector descriptor")
    discipline = models.CharField(max_length=100, choices=DISCIPLINE_CHOICES, default='Web & Experience Systems')
    market = models.CharField(max_length=100, choices=MARKET_CHOICES, default='Dubai')
    year = models.CharField(max_length=10, default='2026')
    hero_image = models.TextField(blank=True, help_text="Hero image URL or data URI")
    summary = models.TextField(help_text="Short teaser summary displayed on cards")
    challenge = models.TextField(blank=True, help_text="The commercial challenge faced by the client")
    solution = models.TextField(blank=True, help_text="The strategic execution by Spec Media")
    deliverables = models.TextField(blank=True, help_text="Comma-separated deliverables (e.g. Design System, Custom Shaders, Headless CMS)")
    kpis = models.TextField(blank=True, help_text="Semicolon-separated KPI results (e.g. +312% Organic Growth; 4.8x ROAS; #1 Dubai Ranking)")
    is_featured = models.BooleanField(default=False, help_text="Feature prominently on homepage and work grid")
    sort_order = models.PositiveIntegerField(default=0, help_text="Display priority (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Work Project"
        verbose_name_plural = "Work Projects"
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.client} · {self.year})"

    def kpi_list(self):
        if not self.kpis:
            return []
        return [k.strip() for k in self.kpis.split(';') if k.strip()]

    def deliverable_list(self):
        if not self.deliverables:
            return []
        return [d.strip() for d in self.deliverables.split(',') if d.strip()]


class SiteSettings(models.Model):
    """
    Global site branding, dynamic logo, favicon, and landing page media & content CMS.
    """
    MEDIA_CHOICES = [
        ('canvas', 'Procedural Kinetic Canvas Engine'),
        ('image', 'Custom Photo / Graphic'),
        ('video', 'Custom Video Loop'),
    ]

    site_name = models.CharField(max_length=150, default="SPEC MEDIA")
    logo_image = models.TextField(blank=True, help_text="Site logo base64 data URI, SVG, or image URL")
    logo_text = models.CharField(max_length=100, default="SPEC MEDIA")
    partner_logos = models.JSONField(default=list, blank=True, help_text="Partner logo URLs or image data URIs displayed in the landing reel")
    capability_photos = models.JSONField(default=dict, blank=True, help_text="Capability example photos keyed by capability name")
    client_reviews = models.JSONField(default=list, blank=True, help_text="Custom client reviews for Instagram cards")
    favicon_image = models.TextField(blank=True, help_text="Favicon base64 data URI, ICO, or SVG")
    
    # Landing Page Content & Media Controls
    hero_headline = models.CharField(max_length=255, default="You feel the brand before it speaks®")
    hero_subheadline = models.TextField(default="Placeholder copy. Spec Media builds campaigns for companies that care how things feel and how they are perceived over time.")
    hero_badge = models.CharField(max_length=100, default="01 / HERO")
    hero_cta_text = models.CharField(max_length=100, default="[ SCROLL DOWN ]")
    hero_media_type = models.CharField(max_length=50, default="canvas", choices=MEDIA_CHOICES)
    hero_media_url = models.TextField(blank=True, help_text="Uploaded photo or video data URI or URL for hero showcase")

    # Scene 02 Brain Scrub & The Reel Media Controls
    scene2_video_url = models.CharField(max_length=500, blank=True, default="/static/scene2_brain.mp4", help_text="Scene 02 brain scrub video loop or canvas fallback")
    scene2_badge = models.CharField(max_length=100, blank=True, default="02 / SCENE 02")
    scene2_hint = models.CharField(max_length=255, blank=True, default="keep scrolling or drag mouse to play · frame pauses instantly")
    reel_video_url = models.CharField(max_length=500, blank=True, default="/static/reference_video.mp4", help_text="The Reel background showcase video")

    # Studio & Ethos Controls
    studio_headline = models.CharField(max_length=255, blank=True, default="Built for brands that demand cultural resonance.")
    studio_subheadline = models.TextField(blank=True, default="Spec Media is an independent creative studio operating at the intersection of cinematic craft, digital infrastructure, and high-velocity performance marketing.")

    # Global Contact & Footer Info
    contact_email = models.CharField(max_length=150, default="hello@specmedia.co")
    contact_phone = models.CharField(max_length=100, default="+971 4 000 0000")
    contact_address = models.CharField(max_length=255, default="Dubai Design District, Building 3, Dubai, UAE")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"Site Settings ({self.site_name})"

    @classmethod
    def get_settings(cls):
        """
        Singleton getter to retrieve or initialize the active global site settings.
        """
        settings_obj = cls.objects.first()
        if not settings_obj:
            settings_obj = cls.objects.create()
        return settings_obj
