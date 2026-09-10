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
    hero_image = models.CharField(max_length=500, blank=True, help_text="Hero image URL or data URI")
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
