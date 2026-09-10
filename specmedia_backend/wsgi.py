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
