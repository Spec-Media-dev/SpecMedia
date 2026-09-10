# SPEC MEDIA — Creative Production, Brand Strategy & Media Systems

> *"You feel the brand before it speaks®"*

A state-of-the-art digital flagship platform and multi-page application for **Spec Media**, integrating custom canvas animations, scroll-driven kinetic typography, frame scrubbing, and a full Django REST backend wired into a live **Supabase** CRM database.

---

## 🌟 Architecture & Key Features

### 1. Interactive Landing Experience (`/`)
- **Kinetic Scroll-Driven Typography**: Dynamic scroll progress illumination and lift on all headings, paragraph descriptions, tags, and footer elements.
- **Scene 02 Audio Frame Scrubbing**: 120-frame canvas animation rendering dynamic audio waveforms pinned to mouse wheel and touch gestures.
- **Parallax Typography & Logo Motion**: Center hero typography translates and scales seamlessly to the navigation chrome on scroll.
- **Card Hover Physics & Kinetic Tilt**: Selected work cards react with subtle 3D hover blur, perspective shifts, and velocity-responsive tilt.
- **Infinite Velocity Marquee Reel**: Marquee speeds and directions respond dynamically to user scroll momentum.
- **Scene 06 Colour Grade Canvas**: Interactive grading pass canvas reflecting scroll position.
- **Infinite Reviews Carousel**: Auto-scrolling partner testimonials with hover focus pausing.

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
