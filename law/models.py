from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


#Law Docs
class WebDoc(models.Model):
    frbr_url = models.TextField(blank=False)
    document_id = models.IntegerField(db_index=True, null=False)
    short_title = models.TextField(blank=False )
    long_title = models.TextField(blank=True )
    number = models.IntegerField(null=True)
    date = models.DateField(null=True)
    year = models.IntegerField(null=True)
    subtype = models.CharField(max_length=255, blank=True)
    locality = models.CharField(max_length=255, blank=True)
    locality_id =  models.IntegerField(null=True)
    category = models.CharField(max_length=255, blank=True)
    category_id = models.IntegerField(null=True)
    tags = models.TextField(blank=True )

    document_created_at = models.DateTimeField(null=True)
    document_updated_at = models.DateTimeField(null=True)

    is_deleted = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    is_stub = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.short_title

    def get_url(self):
        return reverse('ldp', args=[self.id, slugify(self.short_title),])

    def get_logo_class(self):
        return 'icon-act-'+str(self.document_id)

    def get_absolute_url(self):
        return reverse('ldp', args=[self.id, slugify(self.short_title.encode("utf-8")),])

    class Meta(object):
        db_table = 'web_webdoc'
        verbose_name = 'Law Document'
        verbose_name_plural = 'Law Documents'
        
#XML Data for Law Docs
class WebDocXmlData(models.Model):
    webdoc = models.ForeignKey('WebDoc', on_delete=models.CASCADE,null=False,blank=False,related_name="xmldata")
    xml_data = models.TextField(blank=True)
    nyaaya_xml_data = models.TextField(blank=True)
    toc_json = models.TextField(blank=True)

    def __unicode__(self):
        return self.webdoc.short_title

    class Meta(object):
        db_table = 'web_webdocxmldata'
        verbose_name = 'Law XML Data'
        verbose_name_plural = 'Law XML Data'

#Old explainer blocks attached with Law Docs
class DocExplainerBlock(models.Model):
    webdoc = models.ForeignKey('WebDoc', on_delete=models.CASCADE,null=False,blank=False,related_name="explainer")
    section_id = models.CharField(max_length=255, blank=False)
    text = models.TextField(null=False)
    xml_text = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)  + " - " +  str(self.section_id) + " - " + self.webdoc.short_title
    class Meta(object):
        db_table = 'web_docexplainerblock'
        verbose_name = 'Law Explainer'
        verbose_name_plural = 'Law Explainers'

