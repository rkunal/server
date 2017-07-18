from .models import *
from django.db.models import CharField, Count, Value as V


import logging
logger = logging.getLogger(__name__)

def get_category_name(category_id):
	w = WebDoc.objects.filter(is_deleted=False,category_id=category_id)[:1]
	if w:
		return w[0].category
	else:
		return ''

def get_jurisdiction_name(locality_id):
    locality_name =''
    if int(locality_id) == 0:
        locality_name = 'Others'
    else:
        w = WebDoc.objects.filter(is_deleted=False,locality_id=locality_id)[:1]
        if w:
        	return w[0].locality
        else :
        	return ''

def get_webdoc_items(webDocs):
    docs = []
    for doc in webDocs:
        d = {}
        d['id'] = doc.id
        d['document_id'] = doc.document_id
        d['url'] = doc.get_url()
        d['name'] = doc.short_title
        d['locality'] = doc.locality
        docs.append(d)
    return docs

def get_all_jurisdiction_with_count(category_id=None):
    union_cat = None
    if category_id is None:
        docs = WebDoc.objects.filter(is_deleted=False).exclude(category_id__isnull=True).values("locality_id").annotate(
        num_locality =Count("id")
        ).order_by("locality")
    else:
        docs = WebDoc.objects.filter(is_deleted=False).filter(category_id=category_id).values("locality_id").annotate(
        num_locality =Count("id")
        ).order_by("locality")

    localities = []

    for doc in docs:
        cat = {}
        if category_id is None:
            w = WebDoc.objects.filter(is_deleted=False,locality_id=doc['locality_id'])[:1]
        else:
            w = WebDoc.objects.filter(is_deleted=False,locality_id=doc['locality_id'],category_id=category_id)[:1]

        locality_name = w[0].locality

        if doc['locality_id'] is  None:
            locality_name = 'Others'
            locality_id = 0
        else:
            locality_id = doc['locality_id']



        if category_id is None:
            cat['url'] =  reverse('catalogue-for-jurisdiction', args=[ locality_id, slugify(locality_name),])
        else:

           cat['url'] =  reverse('catalogue-for-category-jurisdiction', args=[category_id, slugify(w[0].category), locality_id, slugify(locality_name),])
        cat['id'] = locality_id
        cat['count'] = doc['num_locality']
        cat['name'] = locality_name + ' Laws'
        if locality_name == 'Union':
            union_cat = cat
        else:
            localities.append(cat)
        if union_cat is not None:
            localities.insert(0,union_cat)
        union_cat = None
    return localities

def get_all_categories_with_count(locality_id=None):
    locality_name = None
    if locality_id is None:
        category = WebDoc.objects.filter(is_deleted=False).exclude(category_id__isnull=True).values("category_id").annotate(
        num_category =Count("id")
        ).order_by("category")
    else:
        if int(locality_id) == 0 :
            locality_name = 'Others'
            category = WebDoc.objects.filter(is_deleted=False).filter(locality_id__isnull=True).exclude(category_id__isnull=True).values("category_id").annotate(
            num_category =Count("id")
            ).order_by("category")
        else:
            category = WebDoc.objects.filter(is_deleted=False).filter(locality_id=locality_id).exclude(category_id__isnull=True).values("category_id").annotate(
            num_category =Count("id")
            ).order_by("category")
    categories = []

    if locality_id is not None and int(locality_id) != 0:
        ll = WebDoc.objects.filter(locality_id=locality_id)[:1]
        locality_name = ll[0].locality

    for doc in category:
        cat = {}
        #@TODO: Fix quick bad code
        w = WebDoc.objects.filter(is_deleted=False,category_id=doc['category_id'])[:1]
        category_name = w[0].category
        #if locality_id is not None and int(locality_id) != 0:
        #    ll = WebDoc.objects.filter(locality_id=locality_id)[:1]
        #   locality_name = ll[0].locality

        cat['id'] = doc['category_id']
        cat['count'] = doc['num_category']
        cat['name'] = category_name
        if locality_id is not None:
            cat['url'] =  reverse('catalogue-for-jurisdiction-category', args=[locality_id, slugify(locality_name), doc['category_id'], slugify(category_name),])
        else:
            cat['url'] =  reverse('catalogue-for-category', args=[doc['category_id'], slugify(category_name),])

        categories.append(cat)
        #logger.debug(cat)

    return categories

def get_webDocs_for_category_jurisdiction(category,locality):
    if int(locality) == 0 :
        return WebDoc.objects.filter(is_deleted=False,category_id=category,locality_id__isnull=True).order_by("short_title")
    else:
        return WebDoc.objects.filter(is_deleted=False,category_id=category,locality_id=locality).order_by("short_title")

