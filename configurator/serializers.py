from rest_framework import serializers
from configurator.models import *

class AppTocExplainerMapSerializer(serializers.Serializer):
	title=serializers.CharField()
	url=serializers.CharField()
	image_desktop=serializers.CharField()



class ExplainerSerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=False)
    short_title = serializers.CharField(allow_blank=True)
    url=serializers.SlugField(allow_blank=False)
    image_desktop =  serializers.URLField(allow_blank=True)
  