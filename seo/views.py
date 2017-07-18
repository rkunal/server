from django.shortcuts import render
from .models import *
from django.utils.html import strip_tags
from .serializers import *
# Create your views here.
class SeoManager(object):
    title = "Nyaaya - India's Laws Explained"
    description = "India's first free online repository of every central and state law. Explained in simple English."
    canonical = ""
    og_type=""
    updated_at = None
    og_image = None
    def __init__(self, url=None):
        if(url):
            try:
                self.staticObj = StaticSeo.objects.get(is_deleted=False,url=url)
                self.is_static=True
            except StaticSeo.DoesNotExist:
                self.is_static=False

    def getSerializer(self):
        seo= {}
        if(self.is_static):
            seo['title'] = self.staticObj.title
            seo['description'] = self.staticObj.og_description
            seo['meta_description'] = self.staticObj.meta_description
            seo['canonical'] = self.staticObj.url
            seo['og_type'] = self.staticObj.og_type
            seo['og_url'] = self.staticObj.url
            if self.staticObj.og_image is not None:
                seo['og_image'] = self.staticObj.og_image.url
            seo['og_title'] = self.staticObj.og_title
            seo['updated_at'] = self.staticObj.updated_at
            seo['og_description'] = self.staticObj.og_description

        else:
            seo['title'] = self.title
            seo['description'] = self.description
            seo['meta_description'] = self.description
            seo['canonical'] = self.canonical
            seo['og_type'] = self.og_type
            seo['og_url'] = self.canonical
            seo['og_image'] = self.og_image
            seo['og_title'] = self.title
            seo['updated_at'] = self.updated_at
            seo['og_description'] = self.description
        return SeoSerializer(seo)

