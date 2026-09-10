"""
WSGI config for specmedia_backend project.

It exposes the WSGI callable as a module-level variable named ``application`` and ``app``.
"""

import os
import sys
from pathlib import Path

# Add project root directory to sys.path so Vercel can resolve all modules
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'specmedia_backend.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application

# If running on Vercel serverless, ensure ephemeral /tmp database is initialized
if os.getenv('VERCEL'):
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        from core.models import SEOPage
        if SEOPage.objects.count() == 0:
            call_command('seed_seo_data')
    except Exception as _e:
        print("Vercel DB initialization note:", _e)
