from law.models import *
from rest_framework import serializers 

class CatalogueWebDocSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	count=serializers.IntegerField()
	name=serializers.CharField()
	url=serializers.URLField()

class CatalogueWebDocJurisdictionSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	document_id=serializers.IntegerField()
	url=serializers.URLField()
	name=serializers.CharField()
	locality=serializers.CharField()

class GuideIntroSerializer(serializers.Serializer):
	data = serializers.CharField()
	short_title = serializers.CharField()
	url = serializers.URLField()
