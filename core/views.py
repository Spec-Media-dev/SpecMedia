import os
import re
import base64
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SEOPage, WorkProject, SiteSettings
from .serializers import LeadSubmissionSerializer, EventTrackingSerializer
from .supabase_service import SupabaseService
import logging

logger = logging.getLogger(__name__)

# -------------------------------------------------------------
# Page Views
# -------------------------------------------------------------

def landing_page(request):
    """
    Renders the Spec Media main landing page with 100% original frontend
    kinetic canvas scrubbing, shaders, typography, and text scroll animations,
    dynamically binding global site settings (logo, favicon, hero copy, and hero media).
    """
    template_path = os.path.join(settings.BASE_DIR, 'core', 'templates', 'landing.html')
    if not os.path.exists(template_path):
        template_path = os.path.join(settings.BASE_DIR, 'index.html')
    with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    try:
        site_settings = SiteSettings.get_settings()
    except Exception:
        site_settings = None

    if site_settings:
        # Dynamic Favicon injection
        fav_url = site_settings.favicon_image or 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="%23201e1d"/><text y=".9em" font-size="80" fill="%23c67139">S</text></svg>'
        fav_tag = f'<link rel="icon" href="{fav_url}">'
        if '<link rel="icon"' in html:
            html = re.sub(r'<link[^>]*rel=["\x27]icon["\x27][^>]*>', fav_tag, html)
        elif '<head>' in html:
            html = html.replace('<head>', f'<head>\n  {fav_tag}')
        elif '<helmet>' in html:
            html = html.replace('<helmet>', f'<helmet>\n  {fav_tag}')

        # Dynamic Logo replacement with kinetic effects
        if site_settings.logo_image:
            html = re.sub(
                r'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAEUcAAAH3[a-zA-Z0-9+/=]+',
                site_settings.logo_image,
                html
            )
            # Add dynamic logo kinetic hover & glow effect
            logo_fx_style = """
<style id="spec-dynamic-logo-style">
  [ref="lettersRef"], [ref="logoRef"] img {
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), filter 0.4s ease;
    filter: drop-shadow(0 0 14px rgba(198, 113, 57, 0.35));
    pointer-events: auto !important;
    cursor: pointer;
  }
  [ref="lettersRef"]:hover, [ref="logoRef"] img:hover {
    transform: scale(1.05) rotate(-0.5deg);
    filter: drop-shadow(0 0 24px rgba(198, 113, 57, 0.65));
  }
</style>
"""
            if '</head>' in html:
                html = html.replace('</head>', f'{logo_fx_style}\n</head>')
            elif '</helmet>' in html:
                html = html.replace('</helmet>', f'{logo_fx_style}\n</helmet>')

        # Dynamic Hero Headline
        if site_settings.hero_headline and site_settings.hero_headline != "You feel the brand before it speaks®":
            html = re.sub(
                r'(<h1[^>]*>)(You feel the brand before it speaks®?)(</h1>)',
                rf'\g<1>{site_settings.hero_headline}\g<3>',
                html
            )

        # Dynamic Hero Subheadline
        if site_settings.hero_subheadline:
            default_sub = "Placeholder copy. Spec Media builds campaigns for companies that care how things feel and how they are perceived over time."
            if default_sub in html and site_settings.hero_subheadline != default_sub:
                html = html.replace(default_sub, site_settings.hero_subheadline)

        # Dynamic Hero CTA Text
        if site_settings.hero_cta_text and site_settings.hero_cta_text != "[ scroll down ]":
            html = html.replace('[ scroll down ]', site_settings.hero_cta_text)

        # Dynamic Hero Custom Media (Photo or Video showcase)
        if site_settings.hero_media_type in ('image', 'video') and site_settings.hero_media_url:
            media_overlay = ""
            if site_settings.hero_media_type == 'image':
                media_overlay = f'<div class="spec-hero-media-backdrop" style="position:absolute;inset:0;background:url(\'{site_settings.hero_media_url}\') center/cover no-repeat;opacity:0.65;mix-blend-mode:luminosity;pointer-events:none;z-index:0;transition:opacity .5s ease;"></div>'
            elif site_settings.hero_media_type == 'video':
                media_overlay = f'<div class="spec-hero-media-backdrop" style="position:absolute;inset:0;overflow:hidden;opacity:0.6;pointer-events:none;z-index:0;"><video src="{site_settings.hero_media_url}" autoplay muted loop playsinline style="width:100%;height:100%;object-fit:cover;"></video></div>'
            
            if 'data-screen-label="01 Hero"' in html and media_overlay:
                html = re.sub(
                    r'(data-screen-label="01 Hero"[^>]*>)',
                    rf'\g<1>\n    {media_overlay}',
                    html
                )

    return HttpResponse(html, content_type='text/html; charset=utf-8')


def login_view(request):
    """
    Renders custom operator authorization screen and handles user authentication.
    """
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    next_url = request.GET.get('next') or request.POST.get('next') or '/dashboard/'
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(next_url)
        else:
            error_message = "Invalid operator username or password. Please verify your credentials."

    return render(request, 'login.html', {
        'next_url': next_url,
        'error_message': error_message,
    })


def logout_view(request):
    """
    Logs out the authenticated operator and returns to the login screen.
    """
    logout(request)
    return redirect('/login/')


def work_page(request):
    """
    Dedicated Work & Portfolio archive page with dynamic database case studies.
    """
    projects = WorkProject.objects.all()
    return render(request, 'work.html', {
        'page_title': 'Selected Work & Case Studies — Spec Media',
        'projects': projects,
    })


def work_detail_page(request, slug):
    """
    Individual Case Study detail view with verified KPIs, challenge, and scope.
    """
    project = get_object_or_404(WorkProject, slug=slug)
    return render(request, 'work_detail.html', {
        'project': project,
    })


def studio_page(request):
    """
    Dedicated Studio page detailing the team, philosophy, and global footprint.
    """
    return render(request, 'studio.html', {
        'page_title': 'The Studio — Spec Media',
    })


def capabilities_page(request):
    """
    Dedicated Capabilities page for Brand Strategy, Production, Media, and Content.
    """
    return render(request, 'capabilities.html', {
        'page_title': 'Capabilities — Spec Media',
    })


def portal_page(request):
    """
    Lead Management and Supabase Pipeline Analytics Dashboard.
    """
    return render(request, 'portal.html', {
        'page_title': 'Pipeline & CRM Portal — Spec Media',
    })


@login_required(login_url='/login/')
def dashboard_page(request):
    """
    Unified Control Dashboard: SEO Management, Works CMS, and Leads Inbox.
    Requires verified operator authentication.
    """
    seo_pages = SEOPage.objects.all()
    works = WorkProject.objects.all()
    site_settings = SiteSettings.get_settings()
    leads_count = 0
    try:
        leads = SupabaseService.fetch_leads(limit=100)
        leads_count = len(leads)
    except Exception:
        pass

    return render(request, 'dashboard.html', {
        'seo_pages': seo_pages,
        'works': works,
        'leads_count': leads_count,
        'site_settings': site_settings,
        'user': request.user,
    })


def custom_404_view(request, exception=None):
    """
    Custom branded 404 error page matching Spec Media dark kinetic aesthetics.
    """
    return render(request, '404.html', status=404)


# -------------------------------------------------------------
# Dynamic Sitemaps & Technical SEO Endpoints
# -------------------------------------------------------------

def sitemap_view(request):
    """
    Generates dynamic XML sitemap conforming to Google Search Console specs,
    covering all indexable canonical SEO routes and published Work case studies.
    """
    canonical_base = "https://www.spec-media.com"
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    # Add SEO Pages
    try:
        pages = SEOPage.objects.filter(is_indexable=True)
        for p in pages:
            url = p.canonical_url or f"{canonical_base}{p.route_path}"
            lastmod = p.updated_at.strftime("%Y-%m-%d")
            priority = "1.0" if p.route_path == "/" else ("0.8" if "/services/" in p.route_path else "0.7")
            xml_lines.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{priority}</priority>\n  </url>")
    except Exception:
        pass

    # Add Case Studies
    try:
        works = WorkProject.objects.all()
        for w in works:
            url = f"{canonical_base}/work/{w.slug}/"
            lastmod = w.updated_at.strftime("%Y-%m-%d")
            xml_lines.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.75</priority>\n  </url>")
    except Exception:
        pass

    xml_lines.append('</urlset>')
    return HttpResponse("\n".join(xml_lines), content_type="application/xml; charset=utf-8")


def robots_txt_view(request):
    """
    Generates dynamic robots.txt referencing canonical sitemap
    and protecting internal admin and dashboard roots.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /portal/",
        "Disallow: /api/",
        "",
        "Sitemap: https://www.spec-media.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


# -------------------------------------------------------------
# Site Settings & Media Upload REST APIs
# -------------------------------------------------------------

class SiteSettingsAPIView(APIView):
    """
    GET /api/settings/ -> Retrieve active global site branding, logo, favicon, and landing media settings
    PUT /api/settings/ -> Update site branding and landing page CMS content
    """
    def get(self, request):
        settings_obj = SiteSettings.get_settings()
        return Response({
            'success': True,
            'settings': {
                'site_name': settings_obj.site_name,
                'logo_image': settings_obj.logo_image,
                'logo_text': settings_obj.logo_text,
                'favicon_image': settings_obj.favicon_image,
                'hero_headline': settings_obj.hero_headline,
                'hero_subheadline': settings_obj.hero_subheadline,
                'hero_badge': settings_obj.hero_badge,
                'hero_cta_text': settings_obj.hero_cta_text,
                'hero_media_type': settings_obj.hero_media_type,
                'hero_media_url': settings_obj.hero_media_url,
                'contact_email': settings_obj.contact_email,
                'contact_phone': settings_obj.contact_phone,
                'contact_address': settings_obj.contact_address,
                'updated_at': settings_obj.updated_at.isoformat() if settings_obj.updated_at else None,
            }
        })

    def put(self, request):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'Operator authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        settings_obj = SiteSettings.get_settings()
        d = request.data
        fields = [
            'site_name', 'logo_image', 'logo_text', 'favicon_image',
            'hero_headline', 'hero_subheadline', 'hero_badge', 'hero_cta_text',
            'hero_media_type', 'hero_media_url',
            'contact_email', 'contact_phone', 'contact_address'
        ]
        for field in fields:
            if field in d:
                setattr(settings_obj, field, d.get(field))

        settings_obj.save()
        return Response({'success': True, 'message': 'Site branding and landing page settings updated successfully.'})


class MediaUploadAPIView(APIView):
    """
    POST /api/upload/ -> Upload media file (photo or video), processes it,
    and returns a base64 Data URI + optional static media URL.
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'Operator authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        file = request.FILES.get('file')
        if not file:
            return Response({'success': False, 'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # 30MB limit
        if file.size > 30 * 1024 * 1024:
            return Response({'success': False, 'error': 'File exceeds maximum limit of 30MB'}, status=status.HTTP_400_BAD_REQUEST)

        content_type = file.content_type or 'image/png'
        file_bytes = file.read()
        b64_str = base64.b64encode(file_bytes).decode('utf-8')
        data_uri = f"data:{content_type};base64,{b64_str}"

        media_url = ""
        try:
            upload_dir = os.path.join(settings.BASE_DIR, 'media', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', file.name)
            file_path = os.path.join(upload_dir, safe_name)
            with open(file_path, 'wb') as f_out:
                f_out.write(file_bytes)
            media_url = f"/media/uploads/{safe_name}"
        except Exception:
            pass

        return Response({
            'success': True,
            'data_uri': data_uri,
            'media_url': media_url or data_uri,
            'filename': file.name,
            'size': file.size,
            'content_type': content_type,
        })


# -------------------------------------------------------------
# SEO Management REST APIs
# -------------------------------------------------------------

class SEOPagesAPIView(APIView):
    """
    GET /api/seo-pages/ -> List all SEO pages
    POST /api/seo-pages/ -> Create a new SEO route
    """
    def get(self, request):
        pages = list(SEOPage.objects.values())
        return Response({'success': True, 'count': len(pages), 'results': pages})

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'Operator authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        d = request.data
        route_path = d.get('route_path', '').strip()
        if not route_path.startswith('/'):
            route_path = '/' + route_path

        seo, created = SEOPage.objects.update_or_create(
            route_path=route_path,
            defaults={
                'page_name': d.get('page_name', 'Custom Page'),
                'meta_title': d.get('meta_title', ''),
                'meta_description': d.get('meta_description', ''),
                'primary_keyword': d.get('primary_keyword', ''),
                'secondary_keywords': d.get('secondary_keywords', ''),
                'canonical_url': d.get('canonical_url', f"https://www.spec-media.com{route_path}"),
                'schema_type': d.get('schema_type', 'Service'),
                'is_indexable': d.get('is_indexable', True),
            }
        )
        return Response({'success': True, 'created': created, 'id': seo.id}, status=status.HTTP_201_CREATED)


class SEOPagesDetailAPIView(APIView):
    """
    GET, PUT, DELETE /api/seo-pages/<id>/
    """
    def get(self, request, pk):
        seo = get_object_or_404(SEOPage, pk=pk)
        return Response({
            'success': True,
            'seo': {
                'id': seo.id,
                'route_path': seo.route_path,
                'page_name': seo.page_name,
                'meta_title': seo.meta_title,
                'meta_description': seo.meta_description,
                'primary_keyword': seo.primary_keyword,
                'secondary_keywords': seo.secondary_keywords,
                'canonical_url': seo.canonical_url,
                'schema_type': seo.schema_type,
                'is_indexable': seo.is_indexable,
            }
        })

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'Operator authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        seo = get_object_or_404(SEOPage, pk=pk)
        d = request.data
        seo.page_name = d.get('page_name', seo.page_name)
        seo.meta_title = d.get('meta_title', seo.meta_title)
        seo.meta_description = d.get('meta_description', seo.meta_description)
        seo.primary_keyword = d.get('primary_keyword', seo.primary_keyword)
        seo.secondary_keywords = d.get('secondary_keywords', seo.secondary_keywords)
        seo.canonical_url = d.get('canonical_url', seo.canonical_url)
        seo.schema_type = d.get('schema_type', seo.schema_type)
        if 'is_indexable' in d:
            seo.is_indexable = d.get('is_indexable')
        seo.save()
        return Response({'success': True, 'message': 'SEO metadata updated.'})

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'Operator authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        seo = get_object_or_404(SEOPage, pk=pk)
        seo.delete()
        return Response({'success': True, 'message': 'SEO route deleted.'})


# -------------------------------------------------------------
# Works & Case Studies REST APIs
# -------------------------------------------------------------

class WorkProjectsAPIView(APIView):
    """
    GET /api/works/ -> List all works
    POST /api/works/ -> Add new work project
    """
    def get(self, request):
        works = list(WorkProject.objects.values())
        return Response({'success': True, 'count': len(works), 'results': works})

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'Operator authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        d = request.data
        title = d.get('title', '').strip()
        if not title:
            return Response({'success': False, 'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

        slug = slugify(title)
        base_slug = slug
        counter = 1
        while WorkProject.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        work = WorkProject.objects.create(
            title=title,
            slug=slug,
            client=d.get('client', ''),
            discipline=d.get('discipline', 'Web & Experience Systems'),
            market=d.get('market', 'Dubai'),
            year=d.get('year', '2026'),
            hero_image=d.get('hero_image', ''),
            summary=d.get('summary', ''),
            challenge=d.get('challenge', ''),
            solution=d.get('solution', ''),
            kpis=d.get('kpis', ''),
            deliverables=d.get('deliverables', ''),
            is_featured=d.get('is_featured', False),
            sort_order=int(d.get('sort_order', 0)),
        )
        return Response({'success': True, 'id': work.id, 'slug': work.slug}, status=status.HTTP_201_CREATED)


class WorkProjectsDetailAPIView(APIView):
    """
    GET, PUT, DELETE /api/works/<id>/
    """
    def get(self, request, pk):
        work = get_object_or_404(WorkProject, pk=pk)
        return Response({
            'success': True,
            'work': {
                'id': work.id,
                'title': work.title,
                'slug': work.slug,
                'client': work.client,
                'discipline': work.discipline,
                'market': work.market,
                'year': work.year,
                'hero_image': work.hero_image,
                'summary': work.summary,
                'challenge': work.challenge,
                'solution': work.solution,
                'kpis': work.kpis,
                'deliverables': work.deliverables,
                'is_featured': work.is_featured,
                'sort_order': work.sort_order,
            }
        })

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'Operator authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        work = get_object_or_404(WorkProject, pk=pk)
        d = request.data
        work.title = d.get('title', work.title)
        work.client = d.get('client', work.client)
        work.discipline = d.get('discipline', work.discipline)
        work.market = d.get('market', work.market)
        work.year = d.get('year', work.year)
        work.hero_image = d.get('hero_image', work.hero_image)
        work.summary = d.get('summary', work.summary)
        work.challenge = d.get('challenge', work.challenge)
        work.solution = d.get('solution', work.solution)
        work.kpis = d.get('kpis', work.kpis)
        work.deliverables = d.get('deliverables', work.deliverables)
        if 'is_featured' in d:
            work.is_featured = d.get('is_featured')
        if 'sort_order' in d:
            work.sort_order = int(d.get('sort_order', 0))
        work.save()
        return Response({'success': True, 'message': 'Work updated.'})

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'Operator authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        work = get_object_or_404(WorkProject, pk=pk)
        work.delete()
        return Response({'success': True, 'message': 'Work deleted.'})


# -------------------------------------------------------------
# REST API Views (Connecting to Supabase Database)
# -------------------------------------------------------------

class ContactSubmitAPIView(APIView):
    """
    POST /api/contact/
    Receives project inquiry / contact message, validates input,
    and creates record in Supabase 'leads' table and 'form_events'.
    """
    def post(self, request):
        serializer = LeadSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "errors": serializer.errors,
                "message": "Please correct the errors in the form."
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        validated_data["page_url"] = validated_data.get("page_url") or request.build_absolute_uri()
        validated_data["referrer"] = validated_data.get("referrer") or request.META.get("HTTP_REFERER", "")

        try:
            record = SupabaseService.submit_lead(validated_data)
            return Response({
                "success": True,
                "message": "Inquiry received. The Spec Media team will be in touch shortly.",
                "lead": {
                    "id": record.get("id"),
                    "name": record.get("name"),
                    "email": record.get("email"),
                    "service": record.get("service"),
                    "status": record.get("status", "new"),
                    "created_at": record.get("created_at"),
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Failed to insert lead into Supabase")
            return Response({
                "success": False,
                "error": str(e),
                "message": "Unable to record inquiry into database. Please try again or email hello@specmedia.co"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeadsListAPIView(APIView):
    """
    GET /api/leads/
    Returns leads stored in Supabase with optional filters for status or market.
    """
    def get(self, request):
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))
        lead_status = request.query_params.get("status")
        market = request.query_params.get("market")

        leads = SupabaseService.fetch_leads(limit=limit, offset=offset, status=lead_status, market=market)
        return Response({
            "success": True,
            "count": len(leads),
            "results": leads
        }, status=status.HTTP_200_OK)


class LeadDetailAPIView(APIView):
    """
    GET, PATCH /api/leads/<id>/
    Fetches or updates a single lead in Supabase.
    """
    def get(self, request, lead_id):
        lead = SupabaseService.fetch_lead_by_id(lead_id)
        if not lead:
            return Response({"success": False, "error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True, "lead": lead}, status=status.HTTP_200_OK)

    def patch(self, request, lead_id):
        updates = request.data
        updated_lead = SupabaseService.update_lead(lead_id, updates)
        if not updated_lead:
            return Response({"success": False, "error": "Failed to update lead"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": True, "lead": updated_lead}, status=status.HTTP_200_OK)


class PipelineStatsAPIView(APIView):
    """
    GET /api/stats/pipeline/
    Returns live pipeline metrics from Supabase view_lead_pipeline_stats.
    """
    def get(self, request):
        stats = SupabaseService.fetch_pipeline_stats()
        return Response({
            "success": True,
            "pipeline": stats
        }, status=status.HTTP_200_OK)


class MarketStatsAPIView(APIView):
    """
    GET /api/stats/market/
    Returns market breakdown from Supabase view_leads_by_market.
    """
    def get(self, request):
        market_stats = SupabaseService.fetch_market_stats()
        return Response({
            "success": True,
            "markets": market_stats
        }, status=status.HTTP_200_OK)


class EventTrackingAPIView(APIView):
    """
    POST /api/events/
    Logs client-side user telemetry events into Supabase form_events.
    """
    def post(self, request):
        serializer = EventTrackingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        SupabaseService.record_event(
            lead_id=d.get("lead_id"),
            event=d.get("event"),
            form_type=d.get("form_type", "telemetry"),
            page_url=d.get("page_url") or request.build_absolute_uri(),
            error_msg=d.get("error_msg")
        )
        return Response({"success": True}, status=status.HTTP_200_OK)


class HealthCheckAPIView(APIView):
    """
    GET /api/health/
    Verifies Django backend and Supabase database connectivity.
    """
    def get(self, request):
        health = SupabaseService.check_health()
        return Response({
            "django": "ok",
            "supabase": health
        }, status=status.HTTP_200_OK)
