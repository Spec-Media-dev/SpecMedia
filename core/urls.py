from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Page views
    path('', views.landing_page, name='landing'),
    path('index.html', views.landing_page, name='landing-html'),
    path('work/', views.work_page, name='work'),
    path('work/<slug:slug>/', views.work_detail_page, name='work-detail'),
    path('studio/', views.studio_page, name='studio'),
    path('capabilities/', views.capabilities_page, name='capabilities'),
    path('portal/', views.portal_page, name='portal'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('404/', views.custom_404_view, name='preview-404'),

    # Technical SEO & Crawlers
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('robots.txt', views.robots_txt_view, name='robots'),

    # REST APIs for SEO & Works CMS
    path('api/seo-pages/', views.SEOPagesAPIView.as_view(), name='api-seo-pages'),
    path('api/seo-pages/<int:pk>/', views.SEOPagesDetailAPIView.as_view(), name='api-seo-pages-detail'),
    path('api/works/', views.WorkProjectsAPIView.as_view(), name='api-works'),
    path('api/works/<int:pk>/', views.WorkProjectsDetailAPIView.as_view(), name='api-works-detail'),

    # REST APIs for Supabase integration
    path('api/contact/', views.ContactSubmitAPIView.as_view(), name='api-contact'),
    path('api/leads/', views.LeadsListAPIView.as_view(), name='api-leads-list'),
    path('api/leads/<str:lead_id>/', views.LeadDetailAPIView.as_view(), name='api-lead-detail'),
    path('api/stats/pipeline/', views.PipelineStatsAPIView.as_view(), name='api-stats-pipeline'),
    path('api/stats/market/', views.MarketStatsAPIView.as_view(), name='api-stats-market'),
    path('api/events/', views.EventTrackingAPIView.as_view(), name='api-events'),
    path('api/health/', views.HealthCheckAPIView.as_view(), name='api-health'),
]
