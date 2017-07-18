from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^traffic-fine/$', views.traffic_fine, name='traffic-fine'),
    url(r'^traffic-fine/(?P<slug>[\w-]+)/$', views.traffic_fine, name='traffic-fine'),
    url(r'^catalogue/$', RedirectView.as_view(pattern_name='catalogue-by-category', permanent=False)),
    url(r'^catalogue/category/$', views.catalogue_by_category, name='catalogue-by-category'),
    url(r'^catalogue/category/(?P<category_id>[0-9]+)/(?P<category_slug>[\w-]+)/$', views.catalogue_for_category, name='catalogue-for-category'),
    url(r'^catalogue/jurisdiction/$', views.catalogue_by_jurisdiction, name='catalogue-by-jurisdiction'),
    url(r'^catalogue/category/(?P<category>[0-9]+)/(?P<category_slug>[\w-]+)/jurisdiction/(?P<locality>[0-9]+)/(?P<jurisdiction_slug>[\w-]+)/$',
        views.catalogue_for_category_for_jurisdiction, name='catalogue-for-category-jurisdiction'),
    url(r'^catalogue/jurisdiction/(?P<locality>[0-9]+)/(?P<jurisdiction_slug>[\w-]+)/category/(?P<category>[0-9]+)/(?P<category_slug>[\w-]+)/$',
        views.catalogue_for_jurisdiction_for_category, name='catalogue-for-jurisdiction-category'),
    url(r'^catalogue/jurisdiction/(?P<locality>[0-9]+)/(?P<jurisdiction_slug>[\w-]+)/$', views.catalogue_for_jurisdiction, name='catalogue-for-jurisdiction'),
    url(r'^guides/$', views.guides, name='guides'),
    url(r'^hi/law-explainers/$', views.law_explainers, name='law-explainers-hin'),
    url(r'^law-explainers/$', views.law_explainers, name='law-explainers'),
    url(r'^law-explainers/(?P<doc_id>[0-9]+)/(?P<slug>[\w-]+)/$', views.guide_intro, name='guide-intro'),
    url(r'^hi/(?P<toc_slug>[\-a-z0-9].+)/$', views.apps_lang, name='app_page_lang'),
    url(r'^(?P<toc_slug>[\-a-z0-9].+)/$', views.apps, name='app_page'),
    url(r'^law/(?P<doc_id>[0-9]+)/(?P<doc_title>[\w-]+)/$', views.ldp, name='ldp'),
]
