import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LeadSubmissionSerializer, EventTrackingSerializer
from .supabase_service import SupabaseService
import logging

logger = logging.getLogger(__name__)

# -------------------------------------------------------------
# Page Views
# -------------------------------------------------------------

def landing_page(request):
    """
    Renders the Spec Media main landing page with 100% original frontend
    animations, assets, and unbundler runtime preserved byte-for-byte.
    """
    template_path = os.path.join(settings.BASE_DIR, 'core', 'templates', 'landing.html')
    with open(template_path, 'rb') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/html; charset=utf-8')

def work_page(request):
    """
    Dedicated Work & Portfolio page with project breakdowns.
    """
    return render(request, 'work.html', {
        'page_title': 'Selected Work — Spec Media',
    })

def studio_page(request):
    """
    Dedicated Studio page detailing the team, philosophy, and global footprint.
    """
    return render(request, 'studio.html', {
        'page_title': 'The Studio — Spec Media',
    })

def capabilities_page(request):
    """
    Dedicated Capabilities page for Brand Strategy, Production, Media, and Content.
    """
    return render(request, 'capabilities.html', {
        'page_title': 'Capabilities — Spec Media',
    })

def portal_page(request):
    """
    Lead Management and Supabase Pipeline Analytics Dashboard.
    """
    return render(request, 'portal.html', {
        'page_title': 'Pipeline & CRM Portal — Spec Media',
    })


# -------------------------------------------------------------
# REST API Views (Connecting to Supabase Database)
# -------------------------------------------------------------

class ContactSubmitAPIView(APIView):
    """
    POST /api/contact/
    Receives project inquiry / contact message, validates input,
    and creates record in Supabase 'leads' table and 'form_events'.
    """
    def post(self, request):
        serializer = LeadSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "errors": serializer.errors,
                "message": "Please correct the errors in the form."
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        
        # Enrich metadata
        validated_data["page_url"] = validated_data.get("page_url") or request.build_absolute_uri()
        validated_data["referrer"] = validated_data.get("referrer") or request.META.get("HTTP_REFERER", "")
        
        try:
            record = SupabaseService.submit_lead(validated_data)
            return Response({
                "success": True,
                "message": "Inquiry received. The Spec Media team will be in touch shortly.",
                "lead": {
                    "id": record.get("id"),
                    "name": record.get("name"),
                    "email": record.get("email"),
                    "service": record.get("service"),
                    "status": record.get("status", "new"),
                    "created_at": record.get("created_at"),
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Failed to insert lead into Supabase")
            return Response({
                "success": False,
                "error": str(e),
                "message": "Unable to record inquiry into database. Please try again or email hello@specmedia.co"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeadsListAPIView(APIView):
    """
    GET /api/leads/
    Returns leads stored in Supabase with optional filters for status or market.
    """
    def get(self, request):
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))
        lead_status = request.query_params.get("status")
        market = request.query_params.get("market")

        leads = SupabaseService.fetch_leads(limit=limit, offset=offset, status=lead_status, market=market)
        return Response({
            "success": True,
            "count": len(leads),
            "results": leads
        }, status=status.HTTP_200_OK)


class LeadDetailAPIView(APIView):
    """
    GET, PATCH /api/leads/<id>/
    Fetches or updates a single lead in Supabase.
    """
    def get(self, request, lead_id):
        lead = SupabaseService.fetch_lead_by_id(lead_id)
        if not lead:
            return Response({"success": False, "error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True, "lead": lead}, status=status.HTTP_200_OK)

    def patch(self, request, lead_id):
        updates = request.data
        updated_lead = SupabaseService.update_lead(lead_id, updates)
        if not updated_lead:
            return Response({"success": False, "error": "Failed to update lead"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": True, "lead": updated_lead}, status=status.HTTP_200_OK)


class PipelineStatsAPIView(APIView):
    """
    GET /api/stats/pipeline/
    Returns live pipeline metrics from Supabase view_lead_pipeline_stats.
    """
    def get(self, request):
        stats = SupabaseService.fetch_pipeline_stats()
        return Response({
            "success": True,
            "pipeline": stats
        }, status=status.HTTP_200_OK)


class MarketStatsAPIView(APIView):
    """
    GET /api/stats/market/
    Returns market breakdown from Supabase view_leads_by_market.
    """
    def get(self, request):
        market_stats = SupabaseService.fetch_market_stats()
        return Response({
            "success": True,
            "markets": market_stats
        }, status=status.HTTP_200_OK)


class EventTrackingAPIView(APIView):
    """
    POST /api/events/
    Logs client-side user telemetry events into Supabase form_events.
    """
    def post(self, request):
        serializer = EventTrackingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        SupabaseService.record_event(
            lead_id=d.get("lead_id"),
            event=d.get("event"),
            form_type=d.get("form_type", "telemetry"),
            page_url=d.get("page_url") or request.build_absolute_uri(),
            error_msg=d.get("error_msg")
        )
        return Response({"success": True}, status=status.HTTP_200_OK)


class HealthCheckAPIView(APIView):
    """
    GET /api/health/
    Verifies Django backend and Supabase database connectivity.
    """
    def get(self, request):
        health = SupabaseService.check_health()
        return Response({
            "django": "ok",
            "supabase": health
        }, status=status.HTTP_200_OK)
