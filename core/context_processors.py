from django.conf import settings

def supabase_context(request):
    """
    Exposes safe, public Supabase config to all Django templates.
    """
    return {
        'SUPABASE_URL': settings.SUPABASE_URL,
        'SUPABASE_PUBLISHABLE_KEY': settings.SUPABASE_PUBLISHABLE_KEY,
    }
