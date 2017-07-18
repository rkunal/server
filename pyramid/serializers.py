from rest_framework import serializers 
from .models import *
class PyramidDocSerializer(serializers.ModelSerializer):
    article_published_date = serializers.SerializerMethodField()
    class Meta:
        model = PyramidDoc
        fields = ('id', 'title', 'plain_text', 'article_published_date')
        #fields = '__all__'

    def get_article_published_date(self, obj):
        return obj.published_date if obj.published_date else obj.updated_at

class AppTOCSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()
    class Meta:
        model = AppTOC
        fields = ('pyramid_doc','name','parent','level','id','app','slug','url','has_children')

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_has_children(self, obj):
        return not obj.is_leaf_node()

class NyaayaAppSerializer(serializers.ModelSerializer):
    #tocs = AppTOCSerializer(many=True, read_only=True)
    class Meta:
        model = NyaayaApp
        fields = ('id', 'title', 'theme','lang')
        #fields = '__all__'

class ExplainerSerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=False)
    short_title = serializers.CharField(allow_blank=True)
    #illustration = serializers.URLField(allow_blank=True)
    url=serializers.SlugField(allow_blank=False)
    image_desktop =  serializers.URLField(allow_blank=True)
    #image_mobile =   serializers.URLField(allow_blank=True)