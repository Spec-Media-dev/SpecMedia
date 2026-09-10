"""
WSGI config for specmedia_backend project.

It exposes the WSGI callable as a module-level variable named ``application`` and ``app``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'specmedia_backend.settings')

application = get_wsgi_application()
app = application
