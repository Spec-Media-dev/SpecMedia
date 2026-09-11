"""
WSGI config for specmedia_backend project.

It exposes the WSGI callable as a module-level variable named ``application`` and ``app``.
"""

import os
import sys
import shutil
from pathlib import Path

# Add project root directory to sys.path so Vercel can resolve all modules
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# If running on Vercel serverless, sync repository database and media assets to writable /tmp
if os.getenv('VERCEL'):
    try:
        # 1. Sync database from repo to /tmp/db.sqlite3 so local data is 100% identical on deployment
        db_source = BASE_DIR / 'db.sqlite3'
        db_target = Path('/tmp') / 'db.sqlite3'
        if not db_target.exists() and db_source.exists():
            shutil.copy2(db_source, db_target)

        # 2. Sync media assets from repo to /tmp/media
        media_source = BASE_DIR / 'media'
        media_target = Path('/tmp') / 'media'
        if media_source.exists() and not media_target.exists():
            shutil.copytree(media_source, media_target, dirs_exist_ok=True)
    except Exception as _e:
        print("Vercel /tmp pre-sync note:", _e)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'specmedia_backend.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application

# Fallback: ensure migrations & seed exist if db was not copied
if os.getenv('VERCEL'):
    try:
        from core.models import SEOPage
        if SEOPage.objects.count() == 0:
            from django.core.management import call_command
            call_command('migrate', interactive=False)
            call_command('seed_seo_data')
    except Exception as _e:
        print("Vercel DB initialization note:", _e)

