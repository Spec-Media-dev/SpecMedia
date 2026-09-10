from rest_framework import serializers

class LeadSubmissionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    company = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    role = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')
    country = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    market = serializers.CharField(max_length=100, required=False, allow_blank=True, default='global')
    service = serializers.CharField(max_length=255, required=False, allow_blank=True, default='Brand strategy')
    move = serializers.CharField(max_length=100, required=False, allow_blank=True, default='scale')
    budget = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    message = serializers.CharField(required=False, allow_blank=True, default='')
    form_type = serializers.CharField(max_length=50, required=False, default='contact')
    utm_source = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    utm_medium = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    utm_campaign = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    utm_content = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    page_url = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
    referrer = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')

class EventTrackingSerializer(serializers.Serializer):
    lead_id = serializers.CharField(max_length=255, required=False, allow_null=True)
    event = serializers.CharField(max_length=100, required=True)
    form_type = serializers.CharField(max_length=100, required=False, default='general')
    page_url = serializers.CharField(max_length=500, required=False, allow_blank=True)
    error_msg = serializers.CharField(required=False, allow_blank=True, allow_null=True)
