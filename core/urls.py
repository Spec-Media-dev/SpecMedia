from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Page views
    path('', views.landing_page, name='landing'),
    path('work/', views.work_page, name='work'),
    path('studio/', views.studio_page, name='studio'),
    path('capabilities/', views.capabilities_page, name='capabilities'),
    path('portal/', views.portal_page, name='portal'),

    # REST APIs for Supabase integration
    path('api/contact/', views.ContactSubmitAPIView.as_view(), name='api-contact'),
    path('api/leads/', views.LeadsListAPIView.as_view(), name='api-leads-list'),
    path('api/leads/<str:lead_id>/', views.LeadDetailAPIView.as_view(), name='api-lead-detail'),
    path('api/stats/pipeline/', views.PipelineStatsAPIView.as_view(), name='api-stats-pipeline'),
    path('api/stats/market/', views.MarketStatsAPIView.as_view(), name='api-stats-market'),
    path('api/events/', views.EventTrackingAPIView.as_view(), name='api-events'),
    path('api/health/', views.HealthCheckAPIView.as_view(), name='api-health'),
]
