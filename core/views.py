import os
import re
import base64
from html import escape
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from functools import wraps
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
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

    try:
        projects = list(WorkProject.objects.all()[:4])
    except Exception:
        projects = []

    partner_logos = [logo for logo in (site_settings.partner_logos if site_settings else []) if logo]
    if partner_logos:
        orbit_cards = []
        for idx, partner in enumerate(partner_logos):
            if isinstance(partner, dict):
                p_name = escape(partner.get('name', f'Partner {idx+1}'))
                p_img = escape(partner.get('image', ''), quote=True)
            else:
                p_name = f'Partner {idx+1}'
                p_img = escape(str(partner), quote=True)
            orbit_cards.append(
                f'<div class="spec-orbit-logo-item" data-index="{idx}" data-pad="1" title="{p_name}">'
                f'<img src="{p_img}" alt="{p_name}" draggable="false" />'
                f'</div>'
            )
        orbit_markup = ''.join(orbit_cards)
        html = re.sub(
            r'(<div id="spec-orbit-logos-container"[^>]*>)[\s\S]*?(</div>\s*<!-- Center Typography Manifesto)',
            rf'\g<1>{orbit_markup}\g<2>',
            html,
            count=1,
        )

        # Dynamic Instagram Reviews
    client_reviews = site_settings.client_reviews if site_settings and isinstance(site_settings.client_reviews, list) else []
    if client_reviews:
        # Loop into 8 cards pool for seamless infinite carousel
        reviews_pool = client_reviews * 2 if len(client_reviews) <= 4 else client_reviews
        ig_cards = []
        for rev in reviews_pool:
            if not isinstance(rev, dict):
                continue
            handle = escape(rev.get('handle', 'partner.voice'))
            role = escape(rev.get('role', 'Executive Partner · Dubai, UAE'))
            location = escape(rev.get('location', 'Dubai HQ'))
            quote = escape(rev.get('quote', 'Outstanding design and digital execution.'))
            avatar = escape(rev.get('avatar', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop'), quote=True)
            img = escape(rev.get('image', 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800&auto=format&fit=crop'), quote=True)
            likes = int(rev.get('likes', 2842))
            tags = escape(rev.get('tags', '#SpecMedia #PartnerOutcome'))
            time_ago = escape(rev.get('time', 'RECENT · VERIFIED'))

            ig_cards.append(
                f'<article data-rv="1" class="ig-card" style="flex:none;width:clamp(310px,26vw,380px);background:color-mix(in oklab, var(--color-neutral-900) 95%, black);border:1px solid rgba(255,255,255,0.08);border-radius:18px;overflow:hidden;box-shadow:0 18px 46px rgba(0,0,0,0.6);display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.16,1,.3,1),box-shadow .35s ease,border-color .35s ease;will-change:transform">'
                f'<div style="display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid rgba(255,255,255,0.06)">'
                f'<div style="display:flex;align-items:center;gap:10px">'
                f'<div style="width:38px;height:38px;border-radius:50%;padding:2px;background:linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);display:grid;place-items:center;flex-shrink:0">'
                f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden;border:2px solid #1a1816;background:#2a2622">'
                f'<img src="{avatar}" alt="{handle}" style="width:100%;height:100%;object-fit:cover;display:block"></div></div>'
                f'<div style="line-height:1.25"><div style="display:flex;align-items:center;gap:4px">'
                f'<span style="font-family:system-ui,-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif;font-size:13px;font-weight:700;color:var(--color-bg)">{handle}</span>'
                f'<svg width="13" height="13" viewBox="0 0 24 24" fill="#3897f0" style="flex-shrink:0"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15l-5-5 1.41-1.41L11 14.17l7.59-7.59L20 8l-9 9z"/></svg>'
                f'</div><div style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;color:var(--color-neutral-400);letter-spacing:.02em">{role}</div></div></div>'
                f'<div style="color:var(--color-neutral-400);cursor:pointer;padding:4px;display:flex;gap:3px"><span style="width:3px;height:3px;border-radius:50%;background:currentColor"></span><span style="width:3px;height:3px;border-radius:50%;background:currentColor"></span><span style="width:3px;height:3px;border-radius:50%;background:currentColor"></span></div></div>'
                f'<div style="position:relative;aspect-ratio:4/3;background:#151413;overflow:hidden;cursor:pointer" ondblclick="handleIGCardDblClick(this)">'
                f'<img data-media="1" src="{img}" alt="{handle} Showcase" draggable="false" style="width:100%;height:100%;object-fit:cover;display:block;transition:transform .7s cubic-bezier(.16,1,.3,1)">'
                f'<div class="ig-heart-pulse" style="position:absolute;inset:0;display:grid;place-items:center;pointer-events:none;opacity:0;transform:scale(0.3);transition:all .35s cubic-bezier(.175,.885,.32,1.275)">'
                f'<svg width="68" height="68" viewBox="0 0 24 24" fill="#ff3040"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg></div>'
                f'<div style="position:absolute;left:10px;bottom:10px;padding:3px 8px;border-radius:999px;background:rgba(0,0,0,0.68);backdrop-filter:blur(6px);color:#fff;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:9px;letter-spacing:.08em;text-transform:uppercase">{location}</div></div>'
                f'<div style="padding:10px 14px 6px;display:flex;align-items:center;justify-content:space-between">'
                f'<div style="display:flex;align-items:center;gap:14px">'
                f'<button type="button" class="ig-btn-like" onclick="toggleIGLike(this)" style="background:none;border:none;padding:0;cursor:pointer;color:var(--color-bg);display:flex;align-items:center;transition:transform .2s ease" aria-label="Like">'
                f'<svg class="heart-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg></button>'
                f'<button type="button" style="background:none;border:none;padding:0;cursor:pointer;color:var(--color-bg);display:flex;align-items:center" aria-label="Comment">'
                f'<svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg></button>'
                f'<button type="button" style="background:none;border:none;padding:0;cursor:pointer;color:var(--color-bg);display:flex;align-items:center" aria-label="Share">'
                f'<svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg></button></div>'
                f'<button type="button" class="ig-btn-save" onclick="toggleIGSave(this)" style="background:none;border:none;padding:0;cursor:pointer;color:var(--color-bg);display:flex;align-items:center" aria-label="Save">'
                f'<svg class="save-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg></button></div>'
                f'<div style="padding:0 14px 4px;font-family:system-ui,-apple-system,BlinkMacSystemFont,sans-serif;font-size:12px;color:var(--color-bg);font-weight:600">'
                f'Liked by <span style="font-weight:700">specmedia</span> and <span class="like-number" data-count="{likes}">{likes:,}</span> others</div>'
                f'<div style="padding:2px 14px 8px;font-family:system-ui,-apple-system,BlinkMacSystemFont,sans-serif;font-size:13px;line-height:1.55;color:var(--color-bg)">'
                f'<span style="font-weight:700;margin-right:6px">{handle}</span><span style="color:var(--color-neutral-300);font-weight:400">{quote}</span></div>'
                f'<div style="padding:0 14px 6px;display:flex;align-items:center;justify-content:space-between"><div style="color:#f59e0b;font-size:12px;letter-spacing:2px">★★★★★</div>'
                f'<div style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;color:var(--color-accent)">{tags}</div></div>'
                f'<div style="padding:0 14px 14px;display:flex;flex-direction:column;gap:4px">'
                f'<span style="font-family:system-ui,-apple-system,sans-serif;font-size:11px;color:var(--color-neutral-500);cursor:pointer">View comments</span>'
                f'<span style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--color-neutral-600)">{time_ago}</span></div>'
                f'</article>'
            )
        if ig_cards:
            reviews_markup = ''.join(ig_cards)
            html = re.sub(
                r'(<div data-rvrow="1"[^>]*>)[\s\S]*?(</div>\s*(?:</div>\s*)?</section>)',
                rf'\g<1>{reviews_markup}\g<2>',
                html,
                count=1,
            )
    capability_photos = site_settings.capability_photos if site_settings and isinstance(site_settings.capability_photos, dict) else {}
    if capability_photos:
        default_fallbacks = {
            'Brand strategy': [
                'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1557804506-669a67965ba0?q=80&w=1200&auto=format&fit=crop'
            ],
            'Campaign production': [
                'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1533750516457-a7f992034fec?q=80&w=1200&auto=format&fit=crop'
            ],
            'Performance media': [
                'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1200&auto=format&fit=crop'
            ],
            'Content systems': [
                'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?q=80&w=1200&auto=format&fit=crop'
            ],
        }
        all_disciplines = ['Brand strategy', 'Campaign production', 'Performance media', 'Content systems']
        panels_html = []
        for cap in all_disciplines:
            photos = capability_photos.get(cap) or default_fallbacks.get(cap, [])
            valid = [p for p in photos if isinstance(p, str) and p.strip()]
            if len(valid) < 2 and cap in default_fallbacks:
                for fb in default_fallbacks[cap]:
                    if fb not in valid:
                        valid.append(fb)
            if not valid:
                valid = default_fallbacks.get(cap, [])

            total_slides = len(valid)
            slides_html = []
            for i, p in enumerate(valid):
                is_first = (i == 0)
                opacity = '1' if is_first else '0'
                transform = 'scale(1)' if is_first else 'scale(1.04)'
                z_index = '2' if is_first else '1'
                slides_html.append(
                    f'<div data-pv-slide="{i}" class="spec-pv-slide" style="position:absolute;inset:0;opacity:{opacity};transform:{transform};transition:opacity .35s cubic-bezier(.16,1,.3,1),transform .4s ease;pointer-events:none;z-index:{z_index};overflow:hidden">'
                    f'<img src="{escape(p, quote=True)}" alt="{escape(cap, quote=True)} {i+1}" style="width:100%;height:100%;object-fit:cover;display:block">'
                    f'</div>'
                )
            slides_markup = '\n            '.join(slides_html)

            dashes_html = []
            for i in range(total_slides):
                w = '16px' if i == 0 else '5px'
                bg = '#c51f2e' if i == 0 else 'rgba(255,255,255,0.3)'
                dashes_html.append(
                    f'<span data-pv-dash="{i}" style="display:inline-block;height:2px;width:{w};border-radius:2px;background:{bg};transition:all .25s ease"></span>'
                )
            dashes_markup = '\n              '.join(dashes_html)

            panels_html.append(
                f'<!-- Gallery: {escape(cap)} -->\n'
                f'          <div data-pv="{escape(cap)}" class="spec-pv-panel" style="position:absolute;inset:0;background:#141312;opacity:0;transform:scale(0.96);filter:blur(4px);transition:opacity .24s cubic-bezier(.16,1,.3,1),transform .26s cubic-bezier(.16,1,.3,1),filter .24s ease;overflow:hidden">\n'
                f'            {slides_markup}\n'
                f'            <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(0,0,0,0) 60%, rgba(0,0,0,0.7) 100%);pointer-events:none;z-index:3"></div>\n'
                f'            <div class="spec-pv-dashes" style="position:absolute;bottom:10px;left:12px;display:flex;align-items:center;gap:4px;z-index:5">\n'
                f'              {dashes_markup}\n'
                f'            </div>\n'
                f'            <div class="spec-pv-counter" style="position:absolute;bottom:8px;right:10px;display:flex;align-items:center;gap:3px;padding:2px 7px;border-radius:999px;background:rgba(0,0,0,0.65);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,0.1);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:9px;color:rgba(255,255,255,0.85);letter-spacing:.08em;z-index:5">\n'
                f'              <span class="spec-pv-num">01</span><span style="opacity:0.4">/</span><span>{total_slides:02d}</span>\n'
                f'            </div>\n'
                f'          </div>'
            )
        idle_html = '<div data-pvidle="1" style="position:absolute;inset:0;display:grid;place-items:center;background:#141312;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--color-neutral-500);transition:opacity .45s ease">SELECT A DISCIPLINE</div>'
        all_panels = '\n          '.join(panels_html) + '\n          ' + idle_html

        collage_container_pattern = r'(<div style="position:relative;aspect-ratio:4/3;overflow:hidden;background:#0d0c0c">)[\s\S]*?(</div>\s*<div ref="\{\{\s*previewLabelRef\s*\}\}")'
        html = re.sub(
            collage_container_pattern,
            rf'\g<1>\n          {all_panels}\n        \g<2>',
            html,
            count=1
        )

    if projects:
        card_layouts = [
            ('1/span 7', '16/10', 'var(--color-neutral-900)', 'var(--color-neutral-500)'),
            ('9/span 4', '4/5', 'var(--color-accent-900)', 'var(--color-accent-300)'),
            ('2/span 4', '4/5', 'var(--color-accent-2-900)', 'var(--color-accent-2-300)'),
            ('7/span 6', '16/10', 'var(--color-neutral-900)', 'var(--color-neutral-500)'),
        ]
        cards = []
        for index, project in enumerate(projects):
            grid_column, aspect_ratio, background, muted_color = card_layouts[index]
            offset = '' if index in (0, 2) else 'margin-top:clamp(40px,10vw,180px);' if index == 1 else 'margin-top:clamp(30px,6vw,110px);'
            tags = project.deliverable_list()[:4] or [project.discipline, project.market]
            tag_markup = ''.join(
                f'<span style="padding:8px 14px;background:color-mix(in oklab, var(--color-text) 78%, transparent);backdrop-filter:blur(6px);color:var(--color-bg);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-size:10px">{escape(tag)}</span>'
                for tag in tags
            )
            if project.hero_image:
                media_markup = f'<img src="{escape(project.hero_image, quote=True)}" alt="{escape(project.title, quote=True)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.22,1,.36,1),filter .8s ease;will-change:transform">'
            else:
                media_markup = f'<span style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:{muted_color}">{escape(project.client)} — {escape(project.year)}</span>'
            cards.append(
                f'<article data-card="1" style="grid-column:{grid_column};{offset}transition:filter .5s cubic-bezier(.22,1,.36,1),opacity .5s ease,transform .5s cubic-bezier(.22,1,.36,1)">'
                f'<div style="position:relative;aspect-ratio:{aspect_ratio};overflow:hidden;background:{background};display:grid;place-items:center">'
                f'<div data-media="1" style="position:absolute;inset:0;display:grid;place-items:center;background:inherit;transition:transform .8s cubic-bezier(.22,1,.36,1),filter .8s ease;will-change:transform">{media_markup}</div>'
                f'<div style="position:absolute;left:var(--space-4);right:var(--space-4);bottom:var(--space-4);display:flex;flex-wrap:wrap;gap:6px">{tag_markup}</div>'
                f'</div><div style="display:flex;align-items:baseline;gap:10px;padding:var(--space-4) 0 var(--space-2)">'
                f'<span style="width:7px;height:7px;border:1px solid var(--color-neutral-500);flex:none;transform:translateY(-4px)"></span>'
                f'<h3 style="margin:0;font-family:var(--font-heading);font-size:clamp(22px,2.4vw,34px);line-height:1.05;color:var(--color-bg)">{escape(project.title)}</h3></div>'
                f'<p style="margin:0;padding-left:17px;max-width:44ch;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-size:11px;line-height:1.9;color:var(--color-neutral-400)">{escape(project.summary)}</p></article>'
            )
        work_grid = '<div data-workgrid="1" style="display:grid;grid-template-columns:repeat(12,1fr);gap:clamp(28px,4vw,72px) clamp(20px,3vw,48px);align-items:start">' + ''.join(cards) + '</div>'
        html = re.sub(
            r'    <div data-workgrid="1"[\s\S]*?    </div>\n  </section>',
            f'    {work_grid}\n  </section>',
            html,
            count=1,
        )
        numeric_years = [int(p.year) for p in projects if p.year.isdigit()]
        year_range = f'{min(numeric_years)} — {max(numeric_years)}' if numeric_years else 'selected work'
        html = html.replace('2024 — 2026 · placeholder projects', f'{year_range} · selected projects')

    if site_settings:
        html = html.replace('hello@specmedia.co', escape(site_settings.contact_email))
        html = html.replace('Placeholder address', escape(site_settings.contact_address))
        html = html.replace('Placeholder city', escape(site_settings.site_name))
        html = html.replace('+00 000 000 000', escape(site_settings.contact_phone))
        html = html.replace('placeholder — concept mockup', f'{escape(site_settings.site_name)} · live portfolio')

    if projects:
        first_summary = escape(projects[0].summary)
        numeric_years = [int(p.year) for p in projects if p.year.isdigit()]
        display_year = max(numeric_years) if numeric_years else 'live'
        html = html.replace('est. placeholder', f'est. {display_year}')
        html = html.replace('Placeholder copy. Send me the real statement and I will set it here verbatim.', first_summary)
        html = html.replace('placeholder quotes', 'client outcomes')

        client_index = 0
        summary_index = 0

        def replace_client_placeholder(match):
            nonlocal client_index
            client = projects[client_index % len(projects)].client
            client_index += 1
            return escape(client)

        def replace_review_placeholder(match):
            nonlocal summary_index
            summary = projects[summary_index % len(projects)].summary
            summary_index += 1
            return escape(summary)

        html = html.replace('portrait placeholder', 'client profile')
        html = re.sub(r'Name placeholder', replace_client_placeholder, html)
        html = re.sub(r'Review quote placeholder[^<]*', replace_review_placeholder, html)

    if site_settings:
        # Dynamic Favicon injection
        fav_url = site_settings.favicon_image or 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="%23201e1d"/><text y=".9em" font-size="80" fill="%239e1b24">S</text></svg>'
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
    filter: drop-shadow(0 0 14px rgba(158, 27, 36, 0.35));
    pointer-events: auto !important;
    cursor: pointer;
  }
  [ref="lettersRef"]:hover, [ref="logoRef"] img:hover {
    transform: scale(1.05) rotate(-0.5deg);
    filter: drop-shadow(0 0 24px rgba(158, 27, 36, 0.65));
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
            hero_subheadline = site_settings.hero_subheadline
            if hero_subheadline == default_sub and projects:
                hero_subheadline = projects[0].summary
            if default_sub in html:
                html = html.replace(default_sub, hero_subheadline)

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

        # Dynamic Hero Badge
        if site_settings.hero_badge and site_settings.hero_badge != "01 / HERO":
            html = html.replace('01 / HERO', escape(site_settings.hero_badge))

        # Dynamic Scene 02 Scrub Controls (Video URL, Badge, Hint)
        if hasattr(site_settings, 'scene2_video_url') and site_settings.scene2_video_url:
            html = re.sub(
                r'(<source src=")/static/scene2_brain\.mp4(" type="video/mp4">)',
                rf'\g<1>{escape(site_settings.scene2_video_url, quote=True)}\g<2>',
                html
            )
            html = re.sub(
                r'(<video id="spec-scene2-video"[^>]*>[\s\S]*?<source src=")[^"]+(")',
                rf'\g<1>{escape(site_settings.scene2_video_url, quote=True)}\g<2>',
                html
            )
        if hasattr(site_settings, 'scene2_badge') and site_settings.scene2_badge:
            html = html.replace('<span>scene 02</span>', f'<span>{escape(site_settings.scene2_badge)}</span>')
        if hasattr(site_settings, 'scene2_hint') and site_settings.scene2_hint:
            default_hint = "keep scrolling or drag mouse to play · frame pauses instantly"
            html = html.replace(default_hint, escape(site_settings.scene2_hint))

        # Dynamic Scene 02 60 FPS Sprite Sheet Config
        scene2_sprite = getattr(site_settings, 'scene2_sprite_url', '') or "https://afbvxvknlgsyinqdcend.supabase.co/storage/v1/object/public/media/sprites/scene2_sprite.jpg"
        scene2_video = getattr(site_settings, 'scene2_video_url', '') or "https://afbvxvknlgsyinqdcend.supabase.co/storage/v1/object/public/media/videos/scene2_brain.mp4"
        scene2_cfg = f"""<script id="spec-scene2-config">
  window.__SPEC_SCENE2_SPRITE_URL = "{escape(scene2_sprite, quote=True)}";
  window.__SPEC_SCENE2_VIDEO_URL = "{escape(scene2_video, quote=True)}";
</script>"""
        if '</head>' in html:
            html = html.replace('</head>', f'{scene2_cfg}\n</head>')
        elif '</helmet>' in html:
            html = html.replace('</helmet>', f'{scene2_cfg}\n</helmet>')

        # Dynamic The Reel Video URL
        if hasattr(site_settings, 'reel_video_url') and site_settings.reel_video_url:
            html = re.sub(
                r'(<source src=")/static/reference_video\.mp4(" type="video/mp4">)',
                rf'\g<1>{escape(site_settings.reel_video_url, quote=True)}\g<2>',
                html
            )
            html = re.sub(
                r'(<video id="spec-reel-video"[^>]*>[\s\S]*?<source src=")[^"]+(")',
                rf'\g<1>{escape(site_settings.reel_video_url, quote=True)}\g<2>',
                html
            )

    return HttpResponse(html, content_type='text/html; charset=utf-8')


def admin_required(view_func):
    """
    Decorator that restricts view access exclusively to authenticated staff/superuser administrators.
    Unauthenticated visitors are redirected to the login screen with ?next=.
    Authenticated non-admins receive a 403 Forbidden with an access-denied message.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        if not (request.user.is_staff or request.user.is_superuser):
            return render(request, 'login.html', {
                'error_message': 'Access denied. The portal is restricted to administrators only.',
                'next_url': request.path,
            }, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def login_view(request):
    """
    Renders custom operator authorization screen and handles user authentication.
    Only allows administrators / staff to log in to access the portal.
    """
    next_url = request.GET.get('next') or request.POST.get('next') or '/dashboard/'
    error_message = None

    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect(next_url)
        else:
            logout(request)
            error_message = "Access denied. The portal is restricted to administrators only."

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            if not (user.is_staff or user.is_superuser):
                error_message = "Access denied. Only administrators have access to this portal."
            else:
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
    try:
        site_settings = SiteSettings.get_settings()
    except Exception:
        site_settings = None
    return render(request, 'studio.html', {
        'page_title': 'The Studio — Spec Media',
        'site_settings': site_settings,
    })


def capabilities_page(request):
    """
    Dedicated Capabilities page for Brand Strategy, Production, Media, and Content.
    """
    return render(request, 'capabilities.html', {
        'page_title': 'Capabilities — Spec Media',
    })


@admin_required
def portal_page(request):
    """
    Lead Management and Supabase Pipeline Analytics Dashboard.
    Requires verified administrator authentication.
    """
    return render(request, 'portal.html', {
        'page_title': 'Pipeline & CRM Portal — Spec Media',
        'user': request.user,
    })


@admin_required
def dashboard_page(request):
    """
    Unified Control Dashboard: SEO Management, Works CMS, and Leads Inbox.
    Requires verified operator authentication.
    """
    seo_pages = SEOPage.objects.all()
    works = WorkProject.objects.all()
    try:
        site_settings = SiteSettings.get_settings()
    except Exception:
        site_settings = None

    cap_dict = site_settings.capability_photos if (site_settings and isinstance(site_settings.capability_photos, dict)) else {}
    capability_photo_fields = [
        {'name': 'Brand strategy', 'photos': cap_dict.get('Brand strategy', [])},
        {'name': 'Campaign production', 'photos': cap_dict.get('Campaign production', [])},
        {'name': 'Performance media', 'photos': cap_dict.get('Performance media', [])},
        {'name': 'Content systems', 'photos': cap_dict.get('Content systems', [])},
    ]
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
        'capability_photo_fields': capability_photo_fields,
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
                'partner_logos': settings_obj.partner_logos,
                'capability_photos': settings_obj.capability_photos,
                'client_reviews': settings_obj.client_reviews,
                'favicon_image': settings_obj.favicon_image,
                'hero_headline': settings_obj.hero_headline,
                'hero_subheadline': settings_obj.hero_subheadline,
                'hero_badge': settings_obj.hero_badge,
                'hero_cta_text': settings_obj.hero_cta_text,
                'hero_media_type': settings_obj.hero_media_type,
                'hero_media_url': settings_obj.hero_media_url,
                'scene2_video_url': settings_obj.scene2_video_url,
                'scene2_sprite_url': settings_obj.scene2_sprite_url,
                'scene2_badge': settings_obj.scene2_badge,
                'scene2_hint': settings_obj.scene2_hint,
                'reel_video_url': settings_obj.reel_video_url,
                'studio_headline': settings_obj.studio_headline,
                'studio_subheadline': settings_obj.studio_subheadline,
                'contact_email': settings_obj.contact_email,
                'contact_phone': settings_obj.contact_phone,
                'contact_address': settings_obj.contact_address,
                'updated_at': settings_obj.updated_at.isoformat() if settings_obj.updated_at else None,
            }
        })

    def put(self, request):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'success': False, 'error': 'Administrator authorization required'}, status=status.HTTP_403_FORBIDDEN)

        settings_obj = SiteSettings.get_settings()
        d = request.data
        fields = [
            'site_name', 'logo_image', 'logo_text', 'favicon_image',
            'partner_logos',
            'capability_photos',
            'client_reviews',
            'hero_headline', 'hero_subheadline', 'hero_badge', 'hero_cta_text',
            'hero_media_type', 'hero_media_url',
            'scene2_video_url', 'scene2_sprite_url', 'scene2_badge', 'scene2_hint',
            'reel_video_url',
            'studio_headline', 'studio_subheadline',
            'contact_email', 'contact_phone', 'contact_address'
        ]
        for field in fields:
            if field in d:
                setattr(settings_obj, field, d.get(field))

        settings_obj.save()
        return Response({'success': True, 'message': 'Site branding and landing page settings updated successfully.'})


def extract_video_hd_frames(video_bytes, out_dir, max_frames=192):
    """
    Extracts high-resolution WebP & JPG frames into out_dir for ultra-crisp 60fps canvas scrubbing.
    """
    try:
        import cv2
        import tempfile
        os.makedirs(out_dir, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        try:
            cap = cv2.VideoCapture(tmp_path)
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total <= 0:
                cap.release()
                return 0

            step = max(1, total // max_frames)
            idx = 0
            count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if idx % step == 0 and count < max_frames:
                    count += 1
                    cv2.imwrite(os.path.join(out_dir, f"frame_{count:03d}.webp"), frame, [cv2.IMWRITE_WEBP_QUALITY, 88])
                    cv2.imwrite(os.path.join(out_dir, f"frame_{count:03d}.jpg"), frame, [cv2.IMWRITE_JPEG_QUALITY, 88])
                idx += 1
            cap.release()
            return count
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
    except Exception as e:
        logger.warning(f"HD frame extraction warning: {e}")
        return 0


def generate_video_sprite_sheet(video_bytes, num_frames=100, cols=10, frame_w=720, frame_h=405):
    """
    Extracts num_frames from video_bytes into a cols x rows grid sprite sheet at 720x405 per cell (7200x4050 high definition).
    Uses high-quality Lanczos4 interpolation for crystal-clear frame fidelity.
    Returns JPEG bytes or None if extraction fails or cv2 is not available.
    """
    try:
        import cv2
        import numpy as np
        import tempfile

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        try:
            cap = cv2.VideoCapture(tmp_path)
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total <= 0:
                cap.release()
                return None

            indices = set(int(i * (total - 1) / (num_frames - 1)) for i in range(num_frames))
            rows = int(np.ceil(num_frames / cols))
            grid = np.zeros((rows * frame_h, cols * frame_w, 3), dtype=np.uint8)

            cur = 0
            slot = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if cur in indices:
                    resized = cv2.resize(frame, (frame_w, frame_h), interpolation=cv2.INTER_LANCZOS4)
                    r = slot // cols
                    c = slot % cols
                    if r < rows and c < cols:
                        grid[r*frame_h:(r+1)*frame_h, c*frame_w:(c+1)*frame_w] = resized
                    slot += 1
                cur += 1
            cap.release()

            if slot == 0:
                return None

            success, buf = cv2.imencode('.jpg', grid, [cv2.IMWRITE_JPEG_QUALITY, 92])
            if success:
                return buf.tobytes()
            return None
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
    except Exception as e:
        logger.warning(f"Sprite sheet generation warning: {e}")
        return None


def strip_video_audio(video_bytes):
    """
    Strips all audio tracks from video_bytes losslessly with zero quality re-encoding.
    Returns audio-free MP4 bytes, or original video_bytes if ffmpeg is unavailable.
    """
    try:
        import subprocess, tempfile, imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as in_tmp, \
             tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as out_tmp:
            in_tmp.write(video_bytes)
            in_path = in_tmp.name
            out_path = out_tmp.name

        try:
            res = subprocess.run([exe, '-y', '-i', in_path, '-c:v', 'copy', '-an', out_path],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                with open(out_path, 'rb') as f:
                    return f.read()
        finally:
            for p in [in_path, out_path]:
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass
    except Exception as e:
        logger.warning(f"Audio strip warning: {e}")
    return video_bytes


class MediaUploadAPIView(APIView):
    """
    POST /api/upload/ -> Secure media upload endpoint restricted to administrators.
    Automatically generates 100-frame 60 FPS sprite sheets for video uploads.
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'success': False, 'error': 'Administrator authorization required'}, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES.get('file')
        if not file:
            return Response({'success': False, 'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # 30MB limit
        if file.size > 30 * 1024 * 1024:
            return Response({'success': False, 'error': 'File exceeds maximum limit of 30MB'}, status=status.HTTP_400_BAD_REQUEST)

        content_type = file.content_type or 'image/png'
        file_bytes = file.read()
        is_video = content_type.startswith('video/')
        if is_video:
            # Strip all sound/audio tracks so portfolio videos are completely silent
            file_bytes = strip_video_audio(file_bytes)

        safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', file.name)
        b64_str = base64.b64encode(file_bytes[:1024*500]).decode('utf-8') if not is_video else ""
        data_uri = f"data:{content_type};base64,{b64_str}" if b64_str else ""

        media_url = ""
        # 1. Primary: Upload to Supabase Storage for global CDN streaming
        try:
            client = SupabaseService.get_client()
            storage_path = f"uploads/{safe_name}"
            client.storage.from_('media').upload(
                storage_path,
                file_bytes,
                file_options={'upsert': 'true', 'content-type': content_type}
            )
            media_url = client.storage.from_('media').get_public_url(storage_path)
        except Exception as e:
            logger.warning(f"Supabase Storage upload fallback: {e}")

        # 2. Local disk fallback
        try:
            upload_dir = os.path.join(settings.BASE_DIR, 'media', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, safe_name)
            with open(file_path, 'wb') as f_out:
                f_out.write(file_bytes)
            if not media_url:
                media_url = f"/media/uploads/{safe_name}"
        except Exception:
            pass

        # 3. Automatic 60 FPS Sprite Sheet & Full HD Frame Extraction for Videos
        sprite_url = ""
        is_video = content_type.startswith('video/')
        if is_video:
            try:
                extract_video_hd_frames(file_bytes, os.path.join(settings.BASE_DIR, 'static', 'hd_frames'))
            except Exception as e:
                logger.warning(f"HD frame extraction error: {e}")

            sprite_bytes = generate_video_sprite_sheet(file_bytes)
            if sprite_bytes:
                sprite_filename = f"sprites/{os.path.splitext(safe_name)[0]}_sprite.jpg"
                try:
                    client = SupabaseService.get_client()
                    client.storage.from_('media').upload(
                        sprite_filename,
                        sprite_bytes,
                        file_options={'upsert': 'true', 'content-type': 'image/jpeg'}
                    )
                    sprite_url = client.storage.from_('media').get_public_url(sprite_filename)
                except Exception as e:
                    logger.warning(f"Failed to upload sprite to Supabase: {e}")

                try:
                    sprite_local_dir = os.path.join(settings.BASE_DIR, 'static', 'sprites')
                    os.makedirs(sprite_local_dir, exist_ok=True)
                    sprite_local_path = os.path.join(sprite_local_dir, f"{os.path.splitext(safe_name)[0]}_sprite.jpg")
                    with open(sprite_local_path, 'wb') as f_sp:
                        f_sp.write(sprite_bytes)
                    if not sprite_url:
                        sprite_url = f"/static/sprites/{os.path.splitext(safe_name)[0]}_sprite.jpg"
                except Exception:
                    pass

        # 4. Validate media URL (never use huge base64 data URIs for videos)
        if not media_url:
            if not is_video and len(file_bytes) < 1024 * 1024:
                media_url = data_uri
            else:
                return Response({'success': False, 'error': 'Failed to store video asset in Supabase or local storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'success': True,
            'data_uri': data_uri or media_url,
            'media_url': media_url,
            'sprite_url': sprite_url,
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
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'success': False, 'error': 'Administrator authorization required'}, status=status.HTTP_403_FORBIDDEN)

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
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'success': False, 'error': 'Administrator authorization required'}, status=status.HTTP_403_FORBIDDEN)

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
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'success': False, 'error': 'Administrator authorization required'}, status=status.HTTP_403_FORBIDDEN)

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
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'success': False, 'error': 'Administrator authorization required'}, status=status.HTTP_403_FORBIDDEN)

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
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'success': False, 'error': 'Administrator authorization required'}, status=status.HTTP_403_FORBIDDEN)

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
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'success': False, 'error': 'Administrator authorization required'}, status=status.HTTP_403_FORBIDDEN)

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
    Restricted exclusively to administrators.
    """
    permission_classes = [IsAdminUser]

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
    Restricted exclusively to administrators.
    """
    permission_classes = [IsAdminUser]

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
    Restricted exclusively to administrators.
    """
    permission_classes = [IsAdminUser]

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
    Restricted exclusively to administrators.
    """
    permission_classes = [IsAdminUser]

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
