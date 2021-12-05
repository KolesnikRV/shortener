from django.db.models import fields
from rest_framework import serializers

from url.models import Url


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = serializers.ALL_FIELDS# ('full_url', 'short_url')
