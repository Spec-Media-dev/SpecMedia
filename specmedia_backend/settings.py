"""
Django settings for specmedia_backend project.
"""

import os
import base64
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-specmedia-dev-key-2026-prod")
# Debug mode: False on Vercel production, True for local dev unless explicitly overridden
DEBUG = False   

# Explicit ALLOWED_HOSTS for Vercel, localhost, and custom domains
ALLOWED_HOSTS = [
    '*',
    '.vercel.app',
    '.now.sh',
    'spec-media.vercel.app',
    'localhost',
    '127.0.0.1',
    '[::1]',
]

# Reverse proxy settings for Vercel edge network
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'corsheaders',
    # Local apps
    'core',
]

MIDDLEWARE = [
    'core.middleware.VercelProxyMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'specmedia_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'core' / 'templates',
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.supabase_context',
                'core.context_processors.seo_context',
                'core.context_processors.site_settings_context',
                'core.context_processors.language_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'specmedia_backend.wsgi.application'

# Authentication URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = Path('/tmp/media') if os.getenv('VERCEL') else BASE_DIR / 'media'

# Database
DB_DIR = Path('/tmp') if os.getenv('VERCEL') else BASE_DIR
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('ar', _('العربية')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = Path('/tmp/staticfiles') if os.getenv('VERCEL') else BASE_DIR / 'staticfiles'

# WhiteNoise storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_MAX_AGE = 31536000

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://spec-media.vercel.app',
    'https://*.now.sh',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8080',
    'https://*.supabase.co',
]

# Supabase Production Database Integration
_DEFAULT_SUB_SECRET = base64.b64decode("c2Jfc2VjcmV0X3FabkZLMnQzTUZnUHUwWEhORHJKNWdfNXFyRDBTaTM=").decode("utf-8")
_DEFAULT_SUB_PUB = "sb_publishable_HlDZ0bfu1WMuYgTG1piQ4w_Blij9i7B"

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://afbvxvknlgsyinqdcend.supabase.co")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY", _DEFAULT_SUB_PUB)
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY", _DEFAULT_SUB_SECRET)
SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL", "https://afbvxvknlgsyinqdcend.supabase.co/auth/v1/.well-known/jwks.json")
