from __future__ import unicode_literals
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.db.models import Q
import os
import json
from mptt.templatetags.mptt_tags import cache_tree_children
from stdimage.models import StdImageField
import uuid
import logging
logger = logging.getLogger(__name__)

def upload_to_config_illustrations(instance, filename):
    path = "pyramid_app/config/illustrations/"
    extension = filename.split(".")[-1]
    name = "{}.{}".format(uuid.uuid4(), extension)
    return os.path.join(path, name)

class NyaayaApp(models.Model):
    WOLF = 'DN'
    CHEETAH = 'DU'
    BLOG = 'BL'
    STATIC = 'ST'
    DEFAULT = 'AA'
    THEME_CHOICES = (
        (WOLF, 'Explainers : Dummy-parent Doc without right Nav'),
        (CHEETAH, '---- : Dummy-parent Doc without Nav'),
        (BLOG, 'Blog : Theme with published date'),
        (STATIC, 'Static : Theme for static pages'),
        (DEFAULT,'Guides : Default Theme for Readbility')
    )
    ENG = 'EN'
    HINDI = 'HIN'
    LANG_DEFAULT = 'EN'
    LANG_CHOICES = (
        (ENG, 'English'),
        (HINDI, 'Hindi'),
    )
    title = models.CharField(max_length=225, unique=False)
    theme = models.CharField(max_length=2,choices=THEME_CHOICES, default=DEFAULT, db_index=True)
    lang = models.CharField(max_length=5,choices=LANG_CHOICES, default=LANG_DEFAULT)
    illustration = StdImageField(upload_to=upload_to_config_illustrations, blank=True, null=True, variations={
        'desktop': {"width": 700, "height" : 500, "crop": True},
        'mobile' : {"width": 280, "height" : 200, "crop": True},
    })

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.lang)

    class Meta(object):
        db_table = 'pyramid_nyaayaapp'
        verbose_name = 'App Config'
        verbose_name_plural = 'App Configs'


class PyramidDoc(models.Model):
    title = models.TextField(blank=False)
    raw_content_state = models.TextField(blank=True)
    plain_text = models.TextField(blank=True)

    is_deleted = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    published_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta(object):
        db_table = 'pyramid_pyramiddoc'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        permissions = (
            ("can_publish", "Can publish articles"),
        )

def upload_to_toc_illustrations(instance, filename):
    path = "pyramid_app/toc/illustrations/"
    extension = filename.split(".")[-1]
    name = "{}.{}".format(uuid.uuid4(), extension)
    return os.path.join(path, name)

def recursive_node_to_dict(node):
    if node.is_deleted:
        return None
    has_pyramid = False
    if node.pyramid_doc:
        #if node.pyramid_doc.is_draft == False and node.pyramid_doc.is_deleted == False:
        #    return None
        #else:
        has_pyramid = True

    result = {
        'id': node.id,
        'name': node.name,
        'url': node.get_absolute_url(),
        'has_pyramid': has_pyramid,
        'level': node.level
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
    return result

class AppTOC(MPTTModel):
    name = models.CharField(max_length=225)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    slug = models.SlugField(max_length=225, null=True, blank=True)
    app = models.ForeignKey(NyaayaApp, on_delete=models.SET_NULL, related_name='tocs', blank=True, null=True, db_index=True)
    pyramid_doc = models.ForeignKey(PyramidDoc, on_delete=models.SET_NULL, blank=True, null=True)
    illustration = StdImageField(upload_to=upload_to_toc_illustrations, blank=True, null=True, variations={
        'desktop': {"width": 700, "height" : 500, "crop": True},
        'mobile' : {"width": 280, "height" : 200, "crop": True},
    })

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        db_table = 'pyramid_apptoc'
        verbose_name = 'Table of Content'
        verbose_name_plural = 'Table of Contents'

    def __unicode__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        if self.is_root_node():
            while AppTOC.objects.filter(slug=unique_slug,parent=None).exclude(app__title=self.app.title).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
        else:
            for toc in self.get_siblings():
                if toc.slug == slug:
                    unique_slug = '{}-{}'.format(slug, num)
                    num += 1
        return unique_slug

    def get_absolute_url(self):
        if self.app is None or len(self.name) == 0 :
            return ''
        elif self.app.theme == NyaayaApp.CHEETAH:
            return reverse('app_page', args=[slugify(self.name.encode("utf-8")),])
        elif self.app.title is None or len(self.app.title) == 0:
            return ''
        else:
            slugs = []
            for t in self.get_ancestors(include_self=True):
                slugs.append(t.slug.encode("utf-8"))
            if self.app.lang == NyaayaApp.HINDI:
                return reverse('app_page_lang', args=['/'.join(slugs)])
            else:
                return reverse('app_page', args=['/'.join(slugs)])

    def get_next_toc(self):
        qualified_tocs = self.get_root().get_family().exclude(is_deleted=True).exclude(pyramid_doc__isnull=True)
        selectedToc = None

        for q in qualified_tocs.reverse():
            if q.id == self.id:
                break
            selectedToc = q

        if selectedToc:
            return selectedToc
        else:
            return None

    def get_prev_toc(self):
        if self.is_root_node():
            return None

        qualified_tocs = self.get_root().get_family().exclude(is_deleted=True).exclude(pyramid_doc__isnull=True)
        selectedToc = None

        for q in qualified_tocs:
            if q.id == self.id:
                break
            selectedToc = q

        if selectedToc:
            return selectedToc
        else:
            return None

    def get_illustration_url(self):

        if self.illustration is not None and str(self.illustration) != '':
            return self.illustration.desktop.url

        elif self.app.illustration is not None and str(self.app.illustration) !='':
             return self.app.illustration.desktop.url

        else:
            return None

    def get_json(self):
        root_nodes = cache_tree_children(self.get_family())
        dicts = []
        for n in root_nodes:
            dicts.append(recursive_node_to_dict(n))

        return dicts


    def save(self, *args, **kwargs):
        if not self.id:
            super(AppTOC, self).save(*args, **kwargs)

        slug = self._get_unique_slug()
        #Temporary check for unicode titles. we dont want unicode slugs, would rather override them in admin, until better
        if len(slug):
            self.slug = slug
        super(AppTOC, self).save(*args, **kwargs)

