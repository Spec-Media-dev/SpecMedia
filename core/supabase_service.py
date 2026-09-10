import uuid
import logging
from datetime import datetime, timezone
import requests
from django.conf import settings
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseService:
    _client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._client is None:
            try:
                cls._client = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_SECRET_KEY
                )
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                raise e
        return cls._client

    @classmethod
    def check_health(cls):
        """Verifies connection to Supabase database."""
        try:
            headers = {
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
            }
            res = requests.get(
                f"{settings.SUPABASE_URL}/rest/v1/view_lead_pipeline_stats?select=*&limit=1",
                headers=headers,
                timeout=5
            )
            return {
                "status": "healthy" if res.status_code == 200 else "degraded",
                "status_code": res.status_code,
                "supabase_url": settings.SUPABASE_URL,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "supabase_url": settings.SUPABASE_URL,
            }

    @classmethod
    def submit_lead(cls, data: dict) -> dict:
        """
        Inserts a lead record into Supabase 'leads' table and logs event to 'form_events'.
        """
        now_iso = datetime.now(timezone.utc).isoformat()
        lead_id = data.get("id") or str(uuid.uuid4())

        lead_payload = {
            "id": lead_id,
            "created_at": now_iso,
            "updated_at": now_iso,
            "form_type": data.get("form_type", "contact") or "contact",
            "name": data.get("name", "").strip(),
            "email": data.get("email", "").strip(),
            "company": data.get("company", "").strip() or None,
            "role": data.get("role", "").strip() or None,
            "phone": data.get("phone", "").strip() or None,
            "country": data.get("country", "").strip() or None,
            "market": data.get("market", "").strip() or "global",
            "service": data.get("service", "").strip() or "Brand strategy",
            "move": data.get("move", "").strip() or "scale",
            "budget": data.get("budget", "").strip() or None,
            "message": data.get("message", "").strip() or None,
            "utm_source": data.get("utm_source") or None,
            "utm_medium": data.get("utm_medium") or None,
            "utm_campaign": data.get("utm_campaign") or None,
            "utm_content": data.get("utm_content") or None,
            "page_url": data.get("page_url") or None,
            "referrer": data.get("referrer") or None,
            "status": data.get("status", "new") or "new",
            "notes": data.get("notes") or "Submitted via Spec Media web integration",
            "notified_at": now_iso,
            "notified_ok": True,
        }

        # Try client first, fallback to direct REST if needed
        try:
            client = cls.get_client()
            response = client.table("leads").insert(lead_payload).execute()
            created_records = response.data if hasattr(response, "data") else []
            record = created_records[0] if created_records else lead_payload
        except Exception as e:
            logger.warning(f"Supabase client insert failed, attempting REST API: {e}")
            headers = {
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            res = requests.post(
                f"{settings.SUPABASE_URL}/rest/v1/leads",
                headers=headers,
                json=lead_payload,
                timeout=10
            )
            if res.status_code not in (200, 201):
                raise Exception(f"Supabase REST error {res.status_code}: {res.text}")
            resp_json = res.json()
            record = resp_json[0] if isinstance(resp_json, list) and resp_json else lead_payload

        # Log event in form_events
        try:
            cls.record_event(
                lead_id=lead_id,
                event="form_submit",
                form_type=lead_payload["form_type"],
                page_url=lead_payload.get("page_url"),
                error_msg=None
            )
        except Exception as evt_err:
            logger.warning(f"Failed to record form_event: {evt_err}")

        return record

    @classmethod
    def record_event(cls, lead_id: str = None, event: str = "form_submit", form_type: str = "contact", page_url: str = None, error_msg: str = None):
        """Inserts an event record into 'form_events' table."""
        now_iso = datetime.now(timezone.utc).isoformat()
        event_payload = {
            "created_at": now_iso,
            "lead_id": lead_id,
            "event": event,
            "form_type": form_type,
            "page_url": page_url,
            "error_msg": error_msg,
        }

        try:
            client = cls.get_client()
            client.table("form_events").insert(event_payload).execute()
        except Exception as e:
            headers = {
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
                "Content-Type": "application/json"
            }
            requests.post(
                f"{settings.SUPABASE_URL}/rest/v1/form_events",
                headers=headers,
                json=event_payload,
                timeout=5
            )

    @classmethod
    def fetch_leads(cls, limit: int = 50, offset: int = 0, status: str = None, market: str = None):
        """Retrieves leads from Supabase ordered by creation date."""
        try:
            headers = {
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
            }
            params = {
                "select": "*",
                "order": "created_at.desc",
                "limit": limit,
                "offset": offset,
            }
            if status:
                params["status"] = f"eq.{status}"
            if market:
                params["market"] = f"eq.{market}"

            res = requests.get(
                f"{settings.SUPABASE_URL}/rest/v1/leads",
                headers=headers,
                params=params,
                timeout=8
            )
            if res.status_code == 200:
                return res.json()
            return []
        except Exception as e:
            logger.error(f"Error fetching leads: {e}")
            return []

    @classmethod
    def fetch_lead_by_id(cls, lead_id: str):
        """Retrieves a single lead by ID."""
        try:
            headers = {
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
            }
            res = requests.get(
                f"{settings.SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}&select=*&limit=1",
                headers=headers,
                timeout=5
            )
            if res.status_code == 200:
                items = res.json()
                return items[0] if items else None
            return None
        except Exception as e:
            logger.error(f"Error fetching lead {lead_id}: {e}")
            return None

    @classmethod
    def update_lead(cls, lead_id: str, updates: dict):
        """Updates lead fields (such as status or notes)."""
        now_iso = datetime.now(timezone.utc).isoformat()
        payload = {**updates, "updated_at": now_iso}

        try:
            headers = {
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            res = requests.patch(
                f"{settings.SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}",
                headers=headers,
                json=payload,
                timeout=8
            )
            if res.status_code in (200, 204):
                data = res.json() if res.text else payload
                return data[0] if isinstance(data, list) and data else data
            return None
        except Exception as e:
            logger.error(f"Error updating lead {lead_id}: {e}")
            return None

    @classmethod
    def fetch_pipeline_stats(cls):
        """Retrieves aggregated stats from view_lead_pipeline_stats."""
        try:
            headers = {
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
            }
            res = requests.get(
                f"{settings.SUPABASE_URL}/rest/v1/view_lead_pipeline_stats?select=*",
                headers=headers,
                timeout=5
            )
            if res.status_code == 200:
                items = res.json()
                return items[0] if items else {}
            return {}
        except Exception as e:
            logger.error(f"Error fetching pipeline stats: {e}")
            return {}

    @classmethod
    def fetch_market_stats(cls):
        """Retrieves market distribution from view_leads_by_market."""
        try:
            headers = {
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
            }
            res = requests.get(
                f"{settings.SUPABASE_URL}/rest/v1/view_leads_by_market?select=*&order=lead_count.desc",
                headers=headers,
                timeout=5
            )
            if res.status_code == 200:
                return res.json()
            return []
        except Exception as e:
            logger.error(f"Error fetching market stats: {e}")
            return []
