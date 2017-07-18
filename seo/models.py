from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
import uuid
import os
from urlparse import urlparse
import re

def upload_to_seo_static(instance, filename):
    fname_base, fname_ext = os.path.splitext(filename)
    return 'seo/static/%s%s%s' % (
        uuid.uuid4(),
        now().strftime("%H%M%S"),
        fname_ext.lower(),
    )

class StaticSeo(models.Model):
    url = models.TextField(max_length=255, blank=False, unique=True)
    title = models.CharField(max_length=70, blank=False)
    meta_description = models.TextField(max_length=160, blank=False)
    h1 = models.CharField(max_length=70, blank=True)
    lang = models.CharField(max_length=8, default='en', blank=False)
    og_type = models.CharField(max_length=20, blank=True)
    og_title = models.CharField(max_length=70, blank=True)
    og_description = models.TextField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to=upload_to_seo_static, blank=True)
    og_author = models.TextField(max_length=255, blank=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not re.match(r'http(s?)\:', self.url):
            self.url = 'http://' + self.url
        parsed = urlparse(self.url)
        self.url = parsed.path

    def __unicode__(self):
        return u"%s" % self.url

    class Meta:

        db_table='seo_staticseo'
        verbose_name = "SEO/Social Tags for Static Url"
        verbose_name_plural = "SEO/Social Tags for Static Urls"
