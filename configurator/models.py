from __future__ import unicode_literals

from django.db import models
from pyramid.models import *

class AppTOCExplainerMap(models.Model):
    toc = models.ForeignKey(AppTOC, blank=False, null=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.toc.pyramid_doc

    class Meta(object):
    	db_table='web_apptocexplainermap'
        ordering = ['order',]
        verbose_name = 'Law Explainer'
        verbose_name_plural = 'Law Explainers'


class AppTOCHomeExplainerMap(models.Model):
    toc = models.ForeignKey(AppTOC, blank=False, null=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.toc.pyramid_doc.title.encode("utf-8"))

    class Meta(object):
    	db_table='web_apptochomeexplainermap'
        ordering = ['order',]
        verbose_name = 'Law Explainers ( Home )'
        verbose_name_plural = 'Law Explainers ( Home ) '

def upload_to_webdoc_illustrations(instance, filename):
    path = "webdoc/illustrations/"
    ext = filename.split('.')[-1]
    name = slugify(instance.title.encode("utf-8")) + '.' + ext
    return os.path.join(path, name)

def upload_to_webdoc_illustrations_lowres(instance, filename):
    path = "webdoc/illustrations_lowres/"
    ext = filename.split('.')[-1]
    name = slugify(instance.title.encode("utf-8")) + '.' + ext
    return os.path.join(path, name)

def upload_to_webdoc_image(instance, filename):
    path = "webdoc/images/"
    ext = filename.split('.')[-1]
    name = slugify(instance.title.encode("utf-8")) + '.' + ext
    return os.path.join(path, name)
