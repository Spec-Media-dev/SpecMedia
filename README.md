# SPEC MEDIA — Creative Production, Brand Strategy & Media Systems

> *"You feel the brand before it speaks®"*

A state-of-the-art digital flagship platform and multi-page application for **Spec Media**, integrating custom 3D canvas animations, cinematic image slicing, scroll-driven kinetic typography, fullscreen video expansion, and a full Django REST backend wired into a live **Supabase** CRM database.

📖 **Complete Design & Architecture Documentation**: See [WEBSITE_DESIGN_SPECIFICATION.md](file:///c:/Users/acer/Desktop/specmedia/WEBSITE_DESIGN_SPECIFICATION.md) for the exhaustive design system, spatial grids, 8-phase animation lifecycle, API contracts, and bilingual specs.

---

## 🌟 Architecture & Key Features

### 1. Interactive Landing Experience (`/` / `/en/` / `/ar/`)
- **Centered Hero Logo & Parabolic Flight**: Mathematical centering on initial load with animated entrance, ambient breathing pulse, and smooth parabolic flight docking into the navigation chrome on scroll.
- **Section 02 Cinematic Slicing & Fullscreen Video**:
  - Phase 1–3: Distant 3D approach, 6-cube spatial fragmentation with blur and depth tilt, and seamless convergence into a complete image.
  - Phase 4–6: Hold sharp master image $\to$ smooth expansion to **$100\text{vw} \times 100\text{vh}$ edge-to-edge fullscreen video**.
  - Phase 7–8: Smooth contraction to original small window $\to$ pristine static image hold with permanent scroll lock past Section 2.
- **Kinetic Typography**: Scroll progress illumination lifting typography from subtle translucency to bright white.
- **Card Hover Physics & Kinetic Tilt**: Selected work cards react with 3D hover blur, perspective shifts, and velocity-responsive tilt.
- **Strategy Accordion**: Expanding interactive video cards with audio scrub and smooth height accordion physics.
- **Scene 06 Colour Grade Canvas**: Interactive split-canvas grading pass slider.
- **Section 07 3D Client Orbit**: 25 enterprise partner logos orbiting along 3D elliptical tracks.
- **Infinite Reviews Carousel**: Auto-scrolling testimonials with hover pausing.

### 2. Multi-Page Architecture
- **`/` — Main Flagship Landing Experience**
- **`/work/` — Selected Work & Portfolio Archive**: Comprehensive case studies across Brand Strategy, AI Telco systems, and Health campaigns.
- **`/studio/` — The Studio**: Global presence (London, New York, Riyadh), philosophy, leadership, and operational culture.
- **`/capabilities/` — Capabilities & Disciplines**: Deep dives into Brand Strategy, Campaign Production, Performance Media, and Content Systems.
- **`/portal/` — Live Supabase CRM & Pipeline Dashboard**: Real-time analytics, lead status updates, conversion rates, and pipeline management.

### 3. Backend & Supabase Database Integration
- **Django 5.0 + Django REST Framework** serving live APIs:
  - `POST /api/contact/` — Ingests client leads directly into Supabase `leads` and records telemetry in `form_events`.
  - `GET /api/leads/` — Retrieves all leads ordered by creation timestamp.
  - `PATCH /api/leads/<id>/` — Updates lead status (`new`, `contacted`, `qualified`, `won`, `lost`).
  - `GET /api/stats/pipeline/` — Aggregates lead volume, qualification rate, and status breakdown.
  - `GET /api/stats/market/` — Market distribution analytics across Global, MENA, and regional sectors.
  - `POST /api/events/` — Real-time telemetry tracking for user interactions.
  - `GET /api/health/` — Live health check monitoring Django and Supabase connection status.

---

## 🚀 Getting Started Locally

### 1. Requirements
- Python 3.10+
- `pip`

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Spec-Media-dev/SpecMedia.git
cd SpecMedia
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Ensure your Supabase project URL and API keys are specified:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=*

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_PUBLISHABLE_KEY=your-supabase-publishable-key
SUPABASE_SECRET_KEY=your-supabase-secret-key
SUPABASE_JWKS_URL=https://your-project.supabase.co/auth/v1/.well-known/jwks.json
```

### 4. Database Setup & Static Files
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 5. Launch the Development Server
```bash
python manage.py runserver 8080
```
Visit `http://127.0.0.1:8080/` in your browser.

---

## 🛠 Project Structure
```
specmedia/
├── core/
│   ├── templates/
│   │   ├── landing.html        # Flagship landing page with 100% canvas & motion
│   │   ├── work.html           # Portfolio & project showcase
│   │   ├── studio.html         # Studio philosophy & global locations
│   │   ├── capabilities.html   # Detailed discipline breakdowns
│   │   └── portal.html         # Live Supabase CRM analytics dashboard
│   ├── supabase_service.py     # Resilient Supabase client & REST fallback
│   ├── serializers.py          # DRF serializers for leads & events
│   ├── views.py                # Page views & REST API endpoints
│   └── urls.py                 # Core routing
├── specmedia_backend/
│   ├── settings.py             # Django settings & Supabase config
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py
├── static/                     # Global styles & assets
├── staticfiles/                # Collected static assets
├── index.html                  # Standalone bundle entry point
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔒 License
© 2026 Spec Media. All rights reserved. Concept mockup and production platform.
