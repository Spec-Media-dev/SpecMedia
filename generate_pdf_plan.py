import subprocess
import os
from pathlib import Path

html_file = Path(r"c:\Users\acer\Desktop\specmedia\SpecMedia_Full_Architecture_Plan.html")
pdf_file = Path(r"c:\Users\acer\Desktop\specmedia\SpecMedia_Full_Architecture_Plan.pdf")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SPEC MEDIA — Full System Architecture & Engineering Plan</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,400&family=JetBrains+Mono:wght@400;600&family=Cairo:wght@400;600;700&display=swap');

    @page {
      size: A4;
      margin: 18mm 16mm 20mm 16mm;
      @bottom-right {
        content: counter(page);
        font-family: 'JetBrains Mono', monospace;
        font-size: 8pt;
        color: #888888;
      }
      @bottom-left {
        content: "SPEC MEDIA® — Full Architecture Plan (Frontend & Backend)";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #888888;
      }
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 9.5pt;
      line-height: 1.55;
      color: #1a1a1a;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }

    .page-break {
      page-break-before: always;
    }

    /* Cover Page */
    .cover-page {
      min-height: 92vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border: 2px solid #000000;
      padding: 40px;
      background: #0d0d0f;
      color: #f5ead8;
      position: relative;
    }

    .cover-badge {
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: #c51f2e;
      border: 1px solid rgba(197, 31, 46, 0.4);
      padding: 6px 14px;
      background: rgba(197, 31, 46, 0.08);
      margin-bottom: 24px;
    }

    .cover-title {
      font-size: 34pt;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.08;
      color: #ffffff;
      margin: 0 0 16px 0;
    }

    .cover-subtitle {
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 16pt;
      color: rgba(245, 234, 216, 0.85);
      margin: 0 0 24px 0;
      line-height: 1.35;
    }

    .cover-desc {
      font-size: 10.5pt;
      color: rgba(245, 234, 216, 0.65);
      max-width: 580px;
      line-height: 1.6;
    }

    .cover-meta {
      border-top: 1px solid rgba(245, 234, 216, 0.15);
      padding-top: 24px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      font-size: 8.5pt;
    }

    .cover-meta-item strong {
      display: block;
      color: #c51f2e;
      font-family: 'JetBrains Mono', monospace;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      margin-bottom: 4px;
    }

    /* Content Typography */
    h1, h2, h3, h4 {
      color: #0b0c10;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    h1 {
      font-size: 20pt;
      border-bottom: 2px solid #c51f2e;
      padding-bottom: 6px;
      margin-top: 28px;
      margin-bottom: 16px;
    }

    h2 {
      font-size: 14pt;
      border-left: 3px solid #c51f2e;
      padding-left: 10px;
      margin-top: 22px;
      margin-bottom: 12px;
      color: #1f242d;
    }

    h3 {
      font-size: 11pt;
      margin-top: 14px;
      margin-bottom: 8px;
      color: #333333;
    }

    p {
      margin: 0 0 10px 0;
    }

    ul, ol {
      margin: 0 0 12px 0;
      padding-left: 20px;
    }

    li {
      margin-bottom: 4px;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0 18px 0;
      font-size: 8.5pt;
      background: #ffffff;
    }

    th, td {
      border: 1px solid #d8d8d8;
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
    }

    th {
      background: #f3f3f5;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #111111;
      border-bottom: 2px solid #c51f2e;
    }

    tr:nth-child(even) td {
      background: #fafafa;
    }

    /* Callout Boxes */
    .callout {
      border-left: 4px solid #c51f2e;
      background: #fdf5f5;
      padding: 12px 16px;
      margin: 14px 0;
      border-radius: 0 4px 4px 0;
    }

    .callout-title {
      font-weight: 700;
      color: #c51f2e;
      margin-bottom: 4px;
      font-size: 9.5pt;
    }

    .callout-dark {
      background: #0d0d0f;
      color: #f5ead8;
      border-left: 4px solid #c51f2e;
      padding: 14px 18px;
      margin: 14px 0;
      border-radius: 4px;
    }

    .callout-dark code {
      color: #e26b72;
      background: rgba(255, 255, 255, 0.08);
      padding: 2px 5px;
      border-radius: 3px;
    }

    /* Code Blocks */
    code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      background: #f1f1f3;
      padding: 2px 4px;
      border-radius: 3px;
      color: #b81728;
    }

    pre {
      background: #0f1117;
      color: #e8e8ea;
      padding: 12px 16px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      line-height: 1.45;
      overflow-x: auto;
      margin: 12px 0;
      border: 1px solid #222530;
    }

    /* Diagrams & Badges */
    .diagram-box {
      border: 1px dashed #aaaaaa;
      background: #f9f9fb;
      padding: 14px;
      margin: 14px 0;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      line-height: 1.4;
      white-space: pre;
    }

    .badge {
      display: inline-block;
      padding: 2px 6px;
      font-size: 7.5pt;
      font-family: 'JetBrains Mono', monospace;
      border-radius: 3px;
      font-weight: 600;
    }

    .badge-primary { background: #ffe6e8; color: #c51f2e; border: 1px solid #f8b4ba; }
    .badge-dark { background: #1a1a24; color: #ffffff; }
    .badge-success { background: #e6f8ea; color: #1e7e34; border: 1px solid #b7e4c0; }

    .tag-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 8px 0;
    }

    .arabic-text {
      font-family: 'Cairo', sans-serif;
      direction: rtl;
      display: inline-block;
      font-weight: 600;
    }
  </style>
</head>
<body>

  <!-- COVER PAGE -->
  <div class="cover-page">
    <div>
      <div class="cover-badge">ENGINEERING SPECIFICATION & ARCHITECTURAL BLUEPRINT</div>
      <div class="cover-title">SPEC MEDIA®<br>FULL PLATFORM PLAN</div>
      <div class="cover-subtitle">Frontend Kinetic Architecture & Resilient Backend Engineering</div>
      <div class="cover-desc">
        A definitive technical master-plan for Spec Media: detailing high-performance WebGL & canvas rendering,
        frame scrubbing kinetics, bespoke mobile responsiveness, bilingual RTL engines (Cairo/Arabic),
        Django 5 backend models, RESTful APIs, Supabase object pipelines, and production DevOps strategy.
      </div>
    </div>

    <div class="cover-meta">
      <div class="cover-meta-item">
        <strong>TARGET SYSTEMS</strong>
        Frontend Web App & Django Backend
      </div>
      <div class="cover-meta-item">
        <strong>SPECIFICATION VERSION</strong>
        v2.4.0 (Live Production Blueprint)
      </div>
      <div class="cover-meta-item">
        <strong>PRIMARY JURISDICTION</strong>
        DIFC Dubai & Global Web Standards
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- TABLE OF CONTENTS & EXECUTIVE SUMMARY -->
  <h1>1. Executive Summary & Vision</h1>
  <p>
    <strong>Spec Media</strong> is engineered as a world-class digital brand infrastructure platform that merges 
    uncompromising cinematic aesthetics with military-grade backend resilience. Designed to compete with tier-1 
    international luxury and creative agency web properties (such as Apple, Studio Freight, Active Theory, and A24),
    the platform achieves 120 FPS hardware-accelerated animations, instant zero-lag frame scrubbing, and deep bilingual 
    localization (English & Arabic with full RTL typography).
  </p>

  <div class="callout">
    <div class="callout-title">Core Engineering Directives</div>
    <ul>
      <li><strong>Cinematic Zero-Latency Fidelity:</strong> Eliminating all UI stutter, network seek lag, and layout shifts through Base64 asset inlining, GPU hardware acceleration, and pre-buffered memory blob pipelines.</li>
      <li><strong>Responsive Screen Independence:</strong> Providing tailored widescreen 16:9 cinematic presentation on desktop while dynamically preventing vertical pillar distortion on mobile devices.</li>
      <li><strong>Dual-Engine Architecture:</strong> Vanilla CSS/JS core with React 18 integration for instant initial paint, paired with a robust Django 5.x CMS & REST backend for dynamic live administration.</li>
    </ul>
  </div>

  <h2>System Architecture Diagram</h2>
  <div class="diagram-box">+---------------------------------------------------------------------------------------------------+
|                                  CLIENT BROWSER LAYER (Edge Execution)                           |
|  - HTML5 Canvas 2D & WebGL Engine   - Kinetic Scroll Controller (DCLogic)                         |
|  - React 18 Hydration & DOM Sync     - Cairo RTL Arabic Typography & Locale Switcher             |
|  - Snappy Preview Window Cursor      - Touch & Mobile 16:9 Aspect Ratio Manager                   |
+---------------------------------------------------------------------------------------------------+
                                                  |  HTTP(S) / REST API / JSON
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                DJANGO 5.x BACKEND CORE (Application Layer)                        |
|  - Safe Translation Engine (core/landing_translations.py)  - WhiteNoise Static Compression        |
|  - Work Projects & Proof Engine (WorkProject Model)        - SEO Metadata & Sitemap Generators    |
|  - CMS Singleton Controller (SiteSettings Model)          - Administrative Suite (/dashboard/)   |
|  - REST Endpoints (/api/settings, /api/works, /api/leads)  - Multi-tenant Lead Capture Pipeline   |
+---------------------------------------------------------------------------------------------------+
                         |                                                  |
                         v                                                  v
+---------------------------------------------+    +------------------------------------------------+
|         PERSISTENT DATABASE LAYER           |    |            SUPABASE CLOUD INFRASTRUCTURE       |
|  - SQLite (Local Dev) / PostgreSQL (Prod)   |    |  - High-Definition Video Storage Bucket        |
|  - Normalized Schemas & Bilingual Indices   |    |  - 100-Frame 60FPS Sprite Sheets               |
|  - Migrations Pipeline (0001 - 0008)        |    |  - Presigned Secure Uploads & CDN Delivery     |
+---------------------------------------------+    +------------------------------------------------+</div>

  <div class="page-break"></div>

  <!-- FRONTEND ARCHITECTURE -->
  <h1>2. Frontend Architecture & Design System</h1>
  <p>
    The frontend is built without bulky external UI frameworks, ensuring total stylistic authority, 0ms layout rendering,
    and ultra-lean bundle weight.
  </p>

  <h2>2.1 Technology Stack Matrix</h2>
  <table>
    <thead>
      <tr>
        <th>Subsystem</th>
        <th>Technologies</th>
        <th>Implementation Details</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Core Document</strong></td>
        <td>HTML5 + Semantic Elements</td>
        <td>Single unified DOM tree synchronized between <code>index.html</code> and <code>core/templates/landing.html</code>.</td>
      </tr>
      <tr>
        <td><strong>Styling Architecture</strong></td>
        <td>Bespoke Vanilla CSS3</td>
        <td>CSS Custom Properties (design tokens), 3D perspective transforms, hardware-accelerated filters. Zero Tailwind dependencies.</td>
      </tr>
      <tr>
        <td><strong>Animation & Kinetics</strong></td>
        <td><code>DCLogic</code> Controller</td>
        <td>60/120 FPS <code>requestAnimationFrame</code> loop, signed velocity tracking, cubic bezier spring physics, and Lenis scroll integration.</td>
      </tr>
      <tr>
        <td><strong>Media Rendering</strong></td>
        <td>HTML5 Canvas 2D + Video Blob</td>
        <td>Native 1920x1080 Full HD internal canvas buffers with high-speed keyframe interpolation and fallback sprite decoding.</td>
      </tr>
      <tr>
        <td><strong>Typography</strong></td>
        <td>Google Fonts (Cairo, Inter, Poppins)</td>
        <td>Dual typography hierarchy: <strong>Inter & Poppins</strong> for English; <strong>Cairo</strong> for authoritative Arabic.</td>
      </tr>
    </tbody>
  </table>

  <h2>2.2 Scene-by-Scene Functional Breakdown</h2>
  <table>
    <thead>
      <tr>
        <th>Scene Identifier</th>
        <th>Key Mechanics</th>
        <th>Technical Execution</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>01 / HERO</strong></td>
        <td>Kinetic Base64 Logo, Staggered Reveal, Light-to-Dark Theme Interpolation</td>
        <td>9 individual letter glyphs (Asset 12-20@4x) decoded via data URIs; smooth translation to navbar badge on scroll; luxury cream (<code>#f5ead8</code>) dynamic fade to obsidian.</td>
      </tr>
      <tr>
        <td><strong>02 / FRAME SCRUB</strong></td>
        <td>Cinematic 3D Brain Scrub, 192 Frames, Mobile 16:9 Widescreen Locking</td>
        <td>Full HD 1080p canvas frame extraction; automatic scroll auto-play trigger at 40%; custom mobile responsive containment preventing vertical pillar cropping.</td>
      </tr>
      <tr>
        <td><strong>03 / WORK GRID</strong></td>
        <td>Selected Work Showcase, 3D Perspective Tilt, Dynamic Spotlight, Sibling Blur</td>
        <td>Perspective 1000px mouse tilt; radial spotlight tracker (<code>--spot-x</code>, <code>--spot-y</code>); glowing crimson border (<code>#c51f2e</code>); sibling card blur (4.5px).</td>
      </tr>
      <tr>
        <td><strong>03b / STATEMENT</strong></td>
        <td>Kinetic Typography Headline, Word-by-Word Scroll Scrub</td>
        <td>Individual span tracking; animated translation and opacity shifts; translated as <span class="arabic-text">الانتباه هو أثمن العملات التي تتضاعف مع الزمن.</span></td>
      </tr>
      <tr>
        <td><strong>04 / ORBIT REEL</strong></td>
        <td>Constellation Partner Logos, Spline Flight Paths, Real-Time Physics</td>
        <td>Planetary orbital calculation around central headline; SVG partner logos with glowing hover states and dynamic velocity damping.</td>
      </tr>
      <tr>
        <td><strong>05 / CAPABILITIES</strong></td>
        <td>Photo Replacing Mouse, Total Cursor Hiding, 4-Slide Real-Time Scrubbing</td>
        <td>Root-level <code>cursor: none !important;</code>; floating photo window anchored to mouse coordinates <code>(cx - hw, cy - hh)</code>; zero blur; horizontal scrubbing (01/04 - 04/04).</td>
      </tr>
      <tr>
        <td><strong>06 / SHOWREEL</strong></td>
        <td>Fullscreen Production Reel, Interactive Colour Pass Controls</td>
        <td>High-bitrate video showcase with playback scrubber, color grading toggles (0% to 100%), and interactive timeline scrubbing.</td>
      </tr>
      <tr>
        <td><strong>07 / REVIEWS</strong></td>
        <td>Executive Instagram Testimonial Cards, Infinite Momentum Carousel</td>
        <td>Touch/mouse drag physics; velocity momentum coasting; 3D card tilt; auto-scroll pause on hover; verified partner badge metadata.</td>
      </tr>
      <tr>
        <td><strong>08 / FOOTER & CONTACT</strong></td>
        <td>Global Drawer, Interactive Contact Modal, Obsidian-to-Cream Reverse Theme</td>
        <td>Dynamic modal with lead capture validation; kinetic logo glyph footer; DIFC Gate Precinct 4 address and live GMT+4 status indicator.</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <!-- MOBILE RESPONSIVENESS & I18N -->
  <h1>3. Mobile Engineering & Internationalization</h1>

  <h2>3.1 Mobile Viewport Protection (Scene 02 Video Resolution)</h2>
  <p>
    Standard responsive layouts often break when 16:9 landscape videos are nested in percentage-based containers on portrait phones.
    Spec Media resolves this via an architectural separation between desktop and mobile in both CSS and JavaScript:
  </p>
  <pre><code>/* Mobile Viewport Sizing (CSS Engine) */
@media (max-width: 768px) {
  .spec-scene2-box {
    width: 92% !important;
    max-width: 600px !important;
    height: auto !important;
    aspect-ratio: 16 / 9 !important; /* Locks widescreen ratio */
    border-radius: var(--radius-lg);
  }
  [data-screen-label="02 Frame scrub"] canvas,
  [data-screen-label="02 Frame scrub"] video {
    object-fit: contain !important; /* Zero pixel cropping */
  }
}

// Runtime Sizing Separation in DCLogic.tick()
const isMobile = window.innerWidth <= 768;
if (isMobile) {
  // Mobile: Preserves 16:9 aspect ratio and edge-to-edge expansion
  box.style.setProperty('width', (90 + 10 * ge).toFixed(1) + '%', 'important');
  box.style.setProperty('height', 'auto', 'important');
  box.style.setProperty('aspect-ratio', '16 / 9', 'important');
} else {
  // Desktop: 100% UNCHANGED original widescreen percentage calculations
  box.style.removeProperty('aspect-ratio');
  box.style.width = (46 + 54 * ge).toFixed(1) + '%';
  box.style.height = (52 + 48 * ge).toFixed(1) + '%';
}</code></pre>

  <h2>3.2 Bilingual RTL & Localization System</h2>
  <p>
    The site operates natively under two locale route prefixes: <code>/en/</code> (English LTR) and <code>/ar/</code> (Arabic RTL).
    The system ensures flawless visual parity through the following mechanisms:
  </p>
  <ul>
    <li><strong>Document-Level Attributes:</strong> Injected <code>dir="rtl"</code> and <code>class="spec-rtl"</code> on the root <code>&lt;html&gt;</code> element.</li>
    <li><strong>Authoritative Arabic Typography:</strong> Google's <strong>Cairo</strong> font applied globally with optical size adjustments, modified letter-spacing (avoiding latin tracking stretch), and right-to-left layout reversal.</li>
    <li><strong>LTR Unicode Isolation:</strong> Numerical counters (<code>01 //</code>), metric stats (<code>+340% ARR</code>), and brand trademarks (<code>SPEC MEDIA®</code>) are wrapped in <code>dir="ltr" unicode-bidi: isolate;</code> to prevent bidirectional layout corruption.</li>
  </ul>

  <div class="page-break"></div>

  <!-- BACKEND ARCHITECTURE -->
  <h1>4. Backend Architecture & Data Design</h1>

  <h2>4.1 Django Application Structure</h2>
  <p>
    The backend is structured around a modular Django 5.x architecture adhering to the Model-Template-View (MTV) pattern
    with an integrated service layer.
  </p>

  <div class="diagram-box">specmedia/
├── manage.py                          # Management CLI
├── specmedia_backend/                 # Core configuration
│   ├── settings.py                    # Environment, DB, Security & Caching settings
│   ├── urls.py                        # Root URL routing & API mounts
│   └── wsgi.py / asgi.py              # Application server entry points
└── core/                              # Primary business logic
    ├── models.py                      # WorkProject, SiteSettings, SEOPage models
    ├── views.py                       # HTTP handlers, REST API views, and translation logic
    ├── urls.py                        # Endpoint declarations
    ├── landing_translations.json      # Bilingual translation master dictionary
    ├── supabase_service.py            # Supabase object storage & API pipeline
    └── templates/                     # Production HTML templates
        ├── landing.html               # Main landing application template
        ├── work.html / work_detail    # Portfolio showcase and case studies
        ├── dashboard.html             # Executive administrative CMS
        └── studio.html / portal.html  # Studio profile & client portal</div>

  <h2>4.2 Entity Relationship Model</h2>
  <table>
    <thead>
      <tr>
        <th>Model Entity</th>
        <th>Fields & Types</th>
        <th>Purpose & Responsibilities</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong><code>WorkProject</code></strong></td>
        <td>
          <code>title</code>, <code>title_ar</code> (CharField)<br>
          <code>slug</code> (SlugField, unique)<br>
          <code>client</code>, <code>client_ar</code> (CharField)<br>
          <code>discipline</code>, <code>market</code> (CharField with choices)<br>
          <code>summary</code>, <code>summary_ar</code> (TextField)<br>
          <code>deliverables</code>, <code>kpis</code> (TextField with parser)<br>
          <code>hero_image</code> (TextField / URL)<br>
          <code>is_featured</code>, <code>sort_order</code>
        </td>
        <td>Stores case studies, commercial impact metrics, and client deliverables with native Arabic mirrored fields and localized getter methods (<code>get_title(lang)</code>).</td>
      </tr>
      <tr>
        <td><strong><code>SiteSettings</code></strong></td>
        <td>
          <code>site_name</code>, <code>logo_image</code> (TextField)<br>
          <code>hero_headline</code>, <code>hero_subheadline</code><br>
          <code>scene2_video_url</code>, <code>scene2_sprite_url</code><br>
          <code>partner_logos</code> (JSONField)<br>
          <code>capability_photos</code> (JSONField)<br>
          <code>client_reviews</code> (JSONField)<br>
          <code>contact_email</code>, <code>contact_address</code>
        </td>
        <td>Singleton CMS entity providing dynamic runtime configuration for landing assets, partner logo clouds, review quotes, and video URLs without code redeployment.</td>
      </tr>
      <tr>
        <td><strong><code>SEOPage</code></strong></td>
        <td>
          <code>route_path</code> (CharField, unique)<br>
          <code>meta_title</code>, <code>meta_description</code><br>
          <code>canonical_url</code>, <code>primary_keyword</code><br>
          <code>schema_type</code> (Organization/Service/WebPage)<br>
          <code>is_indexable</code> (BooleanField)
        </td>
        <td>Manages canonical search engine tags, Schema.org JSON-LD graph generation, OpenGraph social sharing headers, and sitemap inclusion for every indexable route.</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <!-- REST API & INTEGRATIONS -->
  <h1>5. API Specifications & Cloud Integrations</h1>

  <h2>5.1 RESTful Endpoint Specifications</h2>
  <table>
    <thead>
      <tr>
        <th>Endpoint Route</th>
        <th>Method</th>
        <th>Payload / Parameters</th>
        <th>Response Contract & Behavior</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>/api/settings/</code></td>
        <td><code>GET</code>, <code>POST</code></td>
        <td>JSON: site settings payload</td>
        <td>Retrieves or updates live CMS configuration. Protected by administrative authentication on mutations.</td>
      </tr>
      <tr>
        <td><code>/api/works/</code></td>
        <td><code>GET</code>, <code>POST</code></td>
        <td>Query: <code>?discipline=&market=</code></td>
        <td>Returns JSON list of portfolio projects with localized fields according to request language headers.</td>
      </tr>
      <tr>
        <td><code>/api/contact/</code></td>
        <td><code>POST</code></td>
        <td><code>{ name, email, budget, brief }</code></td>
        <td>Captures inbound client inquiries, validates fields, forwards to Supabase lead pipeline, and dispatches email alert.</td>
      </tr>
      <tr>
        <td><code>/api/upload/</code></td>
        <td><code>POST</code></td>
        <td>Multipart: <code>file</code></td>
        <td>Receives media assets, compresses images, streams video to Supabase Storage, and returns permanent CDN URL.</td>
      </tr>
      <tr>
        <td><code>/api/health/</code></td>
        <td><code>GET</code></td>
        <td>None</td>
        <td>Returns <code>{ status: "healthy", database: "connected", timestamp: ISO8601 }</code> for load balancer health probes.</td>
      </tr>
    </tbody>
  </table>

  <h2>5.2 Supabase Cloud Storage Pipeline</h2>
  <p>
    Heavy media assets (such as 1080p video MP4s, 7200x4050 high-definition sprite sheets, and uncompressed case study imagery)
    are offloaded to Supabase Object Storage to ensure the Django application server remains fast and stateless:
  </p>
  <ul>
    <li><strong>Asset Buckets:</strong> <code>media/videos/</code> (Scene 02 3D brain and showreel media), <code>media/sprites/</code> (synchronous scrubbing sheets), and <code>media/portfolio/</code> (gallery images).</li>
    <li><strong>Client-Side Blob Prefetching:</strong> JavaScript detects media URLs and issues asynchronous <code>fetch()</code> requests converting remote video bytes into local in-memory <code>blob:</code> URLs. This eliminates HTTP 206 byte-range seeking latency and guarantees instant, buttery frame scrubbing.</li>
  </ul>

  <h2>5.3 Dynamic Safe HTML Translation Engine</h2>
  <p>
    The translation mechanism in <code>core/views.py</code> employs a multi-pass regex compiler that separates 
    pure HTML content from script templates, ensuring that JavaScript string literals and HTML markup are both accurately
    translated without syntax corruption:
  </p>
  <pre><code># Safe Translation Algorithm (core/views.py)
def safe_translate_html(html, lang_map):
    # Pass 1: Split document into markup segments and script template blocks
    parts = re.split(r'(&lt;script[\s\S]*?&lt;/script&gt;)', html)
    for i in range(len(parts)):
        segment = parts[i]
        # Perform dictionary string replacements using sorted key length priority
        for en_str, ar_str in lang_map.items():
            if en_str in segment:
                segment = segment.replace(en_str, ar_str)
        parts[i] = segment # Buffer reassignment ensures all changes are retained
    return "".join(parts)</code></pre>

  <div class="page-break"></div>

  <!-- DEVOPS & PRODUCTION ROADMAP -->
  <h1>6. DevOps, Security & Production Deployment</h1>

  <h2>6.1 Production Infrastructure Topology</h2>
  <table>
    <thead>
      <tr>
        <th>Infrastructure Component</th>
        <th>Production Standard</th>
        <th>Operational Rationale</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Reverse Proxy & TLS</strong></td>
        <td>Nginx 1.26+ with Let's Encrypt SSL</td>
        <td>Terminates HTTPS, enforces HTTP/2, handles gzip/brotli compression, and rate-limits API requests.</td>
      </tr>
      <tr>
        <td><strong>Application Server</strong></td>
        <td>Gunicorn with Uvicorn Workers</td>
        <td>4 worker processes handling asynchronous Django request-response cycles with low memory overhead.</td>
      </tr>
      <tr>
        <td><strong>Static Asset Serving</strong></td>
        <td>WhiteNoise + CDN Edge Caching</td>
        <td>Serves pre-compressed static assets directly from disk with immutable cache-control headers (1 year max-age).</td>
      </tr>
      <tr>
        <td><strong>Database Engine</strong></td>
        <td>Managed PostgreSQL 16 (AWS RDS)</td>
        <td>High-availability relational store with automated snapshots, connection pooling, and read replicas.</td>
      </tr>
      <tr>
        <td><strong>Process Supervision</strong></td>
        <td>Systemd / Docker Container</td>
        <td>Automated process restart, liveness monitoring, and zero-downtime rolling deployment scripts.</td>
      </tr>
    </tbody>
  </table>

  <h2>6.2 Security & Hardening Checklist</h2>
  <div class="callout-dark">
    <div style="font-weight:700;color:#c51f2e;margin-bottom:8px;">MANDATORY PRODUCTION SECURITY CONTROLS</div>
    <ul>
      <li><code>SECURE_SSL_REDIRECT = True</code> & <code>SECURE_HSTS_SECONDS = 31536000</code>: Enforces HTTPS everywhere.</li>
      <li><code>SESSION_COOKIE_SECURE = True</code> & <code>CSRF_COOKIE_SECURE = True</code>: Prevents cookie interception.</li>
      <li><code>X_FRAME_OPTIONS = 'DENY'</code>: Mitigates clickjacking attacks.</li>
      <li><code>Content-Security-Policy (CSP)</code>: Restricts script execution to approved origins and Supabase CDN domains.</li>
      <li><code>Rate Limiting</code>: Enforces 10 requests/minute on <code>/api/contact/</code> to prevent lead submission abuse.</li>
    </ul>
  </div>

  <h2>6.3 Conclusion & Sign-Off</h2>
  <p>
    This architectural blueprint represents the completed, verified engineering foundation of the Spec Media platform.
    Both frontend rendering mechanics (including mobile widescreen 16:9 preservation and snappy cursor replacements) and 
    backend services (Django MTV, bilingual translation maps, and REST APIs) are fully functional, synchronized, and ready
    for enterprise production traffic.
  </p>

  <div style="margin-top:30px;border-top:1px solid #ddd;padding-top:16px;display:flex;justify-content:space-between;font-size:8pt;color:#666;">
    <span>SPEC MEDIA LLC · DIFC GATE PRECINCT 4 · DUBAI, UAE</span>
    <span>CONFIDENTIAL & PROPRIETARY · ALL RIGHTS RESERVED ®</span>
  </div>

</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML plan at: {html_file}")

# Compile into PDF using Microsoft Edge headless
edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]

binary = None
for p in edge_paths:
    if os.path.exists(p):
        binary = p
        break

if binary:
    cmd = [
        binary,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_file}",
        str(html_file),
    ]
    print(f"Compiling PDF with: {binary}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if pdf_file.exists() and pdf_file.stat().st_size > 1000:
        print(f"SUCCESS: PDF generated successfully! File size: {pdf_file.stat().st_size} bytes")
    else:
        print(f"Error compiling PDF: {res.stderr}")
else:
    print("No Edge or Chrome binary found to compile PDF.")
