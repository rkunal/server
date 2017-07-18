from rest_framework import serializers
from .models import *

class StaticSeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSeo
        fields = '__all__'

class SeoSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    canonical = serializers.CharField()
    meta_description = serializers.CharField()
    og_title = serializers.CharField()
    og_type = serializers.CharField()
    og_url = serializers.CharField()
    og_image = serializers.CharField()
    updated_at = serializers.DateTimeField()
    og_description = serializers.CharField()
