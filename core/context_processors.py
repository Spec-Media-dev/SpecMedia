import json
from django.conf import settings
from .models import SEOPage, SiteSettings

def supabase_context(request):
    """
    Exposes safe, public Supabase config to all Django templates.
    """
    return {
        'SUPABASE_URL': settings.SUPABASE_URL,
        'SUPABASE_PUBLISHABLE_KEY': settings.SUPABASE_PUBLISHABLE_KEY,
    }


def site_settings_context(request):
    """
    Exposes active global SiteSettings (logo, favicon, hero text, media) to all templates.
    """
    try:
        settings_obj = SiteSettings.get_settings()
    except Exception:
        settings_obj = None
    return {
        'site_settings': settings_obj,
    }


def seo_context(request):
    """
    Queries canonical SEO metadata for the current request path
    and injects titles, descriptions, OpenGraph tags, and JSON-LD structured data.
    """
    path = request.path
    lookup_paths = [path]
    if path.endswith('/') and len(path) > 1:
        lookup_paths.append(path[:-1])
    else:
        lookup_paths.append(path + '/')

    seo_obj = None
    try:
        seo_obj = SEOPage.objects.filter(route_path__in=lookup_paths, is_indexable=True).first()
    except Exception:
        pass

    # Retrieve site settings for fallback logo and name
    try:
        site_settings = SiteSettings.get_settings()
        site_name = site_settings.site_name
        logo_url = site_settings.logo_image or "https://www.spec-media.com/static/img/logo.png"
    except Exception:
        site_name = "Spec Media"
        logo_url = "https://www.spec-media.com/static/img/logo.png"

    if seo_obj:
        title = seo_obj.meta_title
        description = seo_obj.meta_description
        canonical = seo_obj.canonical_url or f"https://www.spec-media.com{path}"
        primary_keyword = seo_obj.primary_keyword
        og_title = seo_obj.og_title or title
        og_desc = seo_obj.og_description or description
        og_image = seo_obj.og_image_url or "https://spec-media.vercel.app/static/img/og-preview.png"
        schema_type = seo_obj.schema_type
    else:
        title = f"{site_name} — Digital Architecture, Growth & Production Agency Dubai"
        description = f"{site_name} is Dubai's premier digital agency specializing in high-performance website development, data-driven SEO, brand architecture, and AI marketing automation."
        canonical = f"https://www.spec-media.com{path}"
        primary_keyword = "digital agency dubai"
        og_title = title
        og_desc = description
        og_image = "https://spec-media.vercel.app/static/img/og-preview.png"
        schema_type = "Organization"

    # Generate JSON-LD Schema.org representation
    json_ld = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": site_name,
        "url": canonical,
        "description": description,
    }
    if schema_type == "Organization":
        json_ld["logo"] = logo_url
        json_ld["address"] = {
            "@type": "PostalAddress",
            "addressLocality": "Dubai",
            "addressRegion": "Dubai",
            "addressCountry": "AE"
        }
        json_ld["sameAs"] = [
            "https://www.linkedin.com/company/spec-media",
            "https://twitter.com/specmedia"
        ]
    elif schema_type == "Service":
        json_ld["provider"] = {
            "@type": "Organization",
            "name": site_name,
            "url": "https://www.spec-media.com"
        }
        json_ld["areaServed"] = ["Dubai", "United Arab Emirates", "MENA"]

    return {
        'page_seo': {
            'title': title,
            'description': description,
            'canonical': canonical,
            'primary_keyword': primary_keyword,
            'og_title': og_title,
            'og_description': og_desc,
            'og_image': og_image,
            'schema_json': json.dumps(json_ld, indent=2),
        }
    }
