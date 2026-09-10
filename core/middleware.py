class VercelProxyMiddleware:
    """
    Middleware to safely normalize host headers when deployed behind
    Vercel reverse proxies and edge routing layers.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Normalize HTTP_X_FORWARDED_HOST if multiple comma-separated hosts are passed
        if "HTTP_X_FORWARDED_HOST" in request.META:
            raw_host = request.META["HTTP_X_FORWARDED_HOST"]
            if "," in raw_host:
                first_host = raw_host.split(",")[0].strip()
                request.META["HTTP_X_FORWARDED_HOST"] = first_host

        # Normalize HTTP_HOST if it contains comma or invalid characters
        if "HTTP_HOST" in request.META:
            raw_host = request.META["HTTP_HOST"]
            if "," in raw_host:
                first_host = raw_host.split(",")[0].strip()
                request.META["HTTP_HOST"] = first_host

        return self.get_response(request)
