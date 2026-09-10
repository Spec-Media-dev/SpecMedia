import json
from django.conf import settings
from .models import SEOPage

def supabase_context(request):
    """
    Exposes safe, public Supabase config to all Django templates.
    """
    return {
        'SUPABASE_URL': settings.SUPABASE_URL,
        'SUPABASE_PUBLISHABLE_KEY': settings.SUPABASE_PUBLISHABLE_KEY,
    }


def seo_context(request):
    """
    Queries canonical SEO metadata for the current request path
    and injects titles, descriptions, OpenGraph tags, and JSON-LD structured data.
    """
    path = request.path
    # Normalize path (ensure leading slash, strip redundant trailing if needed)
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
        title = "Spec Media — Digital Architecture, Growth & Production Agency Dubai"
        description = "Spec Media is Dubai's premier digital agency specializing in high-performance website development, data-driven SEO, brand architecture, and AI marketing automation."
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
        "name": "Spec Media",
        "url": canonical,
        "description": description,
    }
    if schema_type == "Organization":
        json_ld["logo"] = "https://www.spec-media.com/static/img/logo.png"
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
            "name": "Spec Media",
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
