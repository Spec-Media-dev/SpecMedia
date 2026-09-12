from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns
from core import views as core_views

# 1. Top-level unprefixed endpoints (admin, django i18n, switcher, technical SEO, and REST APIs)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('set-language/', core_views.set_language_view, name='root-set-language'),
    path('sitemap.xml', core_views.sitemap_view, name='root-sitemap'),
    path('robots.txt', core_views.robots_txt_view, name='root-robots'),

    # Direct unprefixed REST APIs
    path('api/settings/', core_views.SiteSettingsAPIView.as_view()),
    path('api/upload/', core_views.MediaUploadAPIView.as_view()),
    path('api/seo-pages/', core_views.SEOPagesAPIView.as_view()),
    path('api/seo-pages/<int:pk>/', core_views.SEOPagesDetailAPIView.as_view()),
    path('api/works/', core_views.WorkProjectsAPIView.as_view()),
    path('api/works/<int:pk>/', core_views.WorkProjectsDetailAPIView.as_view()),
    path('api/contact/', core_views.ContactSubmitAPIView.as_view()),
    path('api/leads/', core_views.LeadsListAPIView.as_view()),
    path('api/leads/<str:lead_id>/', core_views.LeadDetailAPIView.as_view()),
    path('api/stats/pipeline/', core_views.PipelineStatsAPIView.as_view()),
    path('api/stats/market/', core_views.MarketStatsAPIView.as_view()),
    path('api/events/', core_views.EventTrackingAPIView.as_view()),
    path('api/health/', core_views.HealthCheckAPIView.as_view()),
]

# 2. Localized page routes with language prefix (/en/, /ar/, /fr/, /es/, /de/)
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    prefix_default_language=True,
)

# 3. Static & Media files
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

handler404 = 'core.views.custom_404_view'

