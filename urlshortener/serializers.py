from rest_framework import serializers
from .models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'code', 'clicks', 'created_at']
        read_only_fields = ['id', 'code', 'clicks', 'created_at']