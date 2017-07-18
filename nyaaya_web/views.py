from django.shortcuts import render
import json
from nyaaya_api.views import (
    HomePage,
    TrafficFineListPage,
    CatalogueByCategories,
    CatalogueForCategory,
    CatalogueByJurisdiction,
    CatalogueByJurisdiction,
    CatalogueForCateoryForJurisdiction,
    CatalogueForJurisdiction,
    GuidesPage,
    CatalogueForJurisdictionForCateory,
    LawExplainersPage,
    GuideIntro,
    WriteToUs,
    AppPage,
)
from django.http import Http404



def index(request):
    api_response = HomePage.as_view()(request).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data.get('seo')
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def traffic_fine(request, slug=None):
    api_response = TrafficFineListPage.as_view()(request).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def catalogue_by_category(request):
    api_response = CatalogueByCategories.as_view()(request).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def catalogue_for_category(request, category_id, category_slug):
    api_response = CatalogueForCategory.as_view()(request, category_id, category_slug).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def catalogue_by_jurisdiction(request):
    api_response = CatalogueByJurisdiction.as_view()(request).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def catalogue_for_category_for_jurisdiction(request, category, category_slug, locality, jurisdiction_slug):
    api_response = CatalogueForCateoryForJurisdiction.as_view()(request, category, category_slug, locality, jurisdiction_slug).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def catalogue_for_jurisdiction(request, locality, jurisdiction_slug):
    api_response = CatalogueForJurisdiction.as_view()(request, locality, jurisdiction_slug).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def catalogue_for_jurisdiction_for_category(request, locality, jurisdiction_slug, category, category_slug):
    api_response = CatalogueForJurisdictionForCateory.as_view()(request, locality, jurisdiction_slug, category, category_slug).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


#@TODO: Hindi Law Explainers
def law_explainers(request):
    api_response = LawExplainersPage.as_view()(request).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def guides(request):
    api_response = GuidesPage.as_view()(request).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})


def guide_intro(request, doc_id, slug=None):
    api_response = GuideIntro.as_view()(request, doc_id, slug=None).render().content
    try:
        shared_data = json.loads(api_response)
        seo = shared_data['seo']
    except:
        shared_data = {}
        seo = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})

def apps_lang(request, toc_slug=None):
    return apps(request,toc_slug,'hi')

def apps(request,toc_slug=None,lang=None):
    seo = {}
    if lang is not None:
        appResponse = AppPage.as_view({'get': 'getlang'})(request,toc_slug,lang).render().content
    else:
        appResponse = AppPage.as_view({'get': 'list'})(request,toc_slug).render().content
    if appResponse is  None or not len(appResponse):
        raise Http404("Not Found")
    try:
        shared_data = json.loads(appResponse)
        seo = shared_data.get('seo',{})
    except ValueError, e:
        shared_data = {}
    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})

def ldp(request, doc_id=None, doc_title=None):
    ldp_response = LDPView.as_view({'get': 'get'})(request, doc_id).render().content
    seo = {}
    try:
        shared_data = json.loads(ldp_response)
        seo = shared_data.get('seo')
    except:
        shared_data = {}

    return render(request, 'nyaaya_web/index.html', {'SHAREDDATA': json.dumps(shared_data), 'seo': seo})
