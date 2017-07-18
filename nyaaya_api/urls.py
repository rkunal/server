from django.conf.urls import url,include
from django.contrib import admin
from nyaaya_api import views
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
    url(r'homepage/',views.HomePage.as_view()),
    url(r'^traffic-fine/$', views.TrafficFineListPage.as_view(), name='traffic-fine'),
    url(r'^traffic-fine/(?P<slug>[\w-]+)/$',views.TrafficFineListPage.as_view(), name='traffic-fine'),
    url(r'^catalogue/category/$', views.CatalogueByCategories.as_view(),name='catalogue-category'),
	url(r'^catalogue/category/(?P<category>[0-9]+)/(?P<category_slug>[\w-]+)/jurisdiction/(?P<locality>[0-9]+)/(?P<jurisdiction_slug>[\w-]+)/$', views.CatalogueForCateoryForJurisdiction.as_view(),name='catalogue-category-jurisdiction'),
	url(r'^catalogue/jurisdiction/$', views.CatalogueByJurisdiction.as_view(),name='catalogue-jurisdiction'),
	url(r'^catalogue/category/(?P<category_id>[0-9]+)/(?P<category_slug>[\w-]+)/$', views.CatalogueForCategory.as_view(),name='catalogue-category'),
	url(r'^catalogue/jurisdiction/(?P<locality>[0-9]+)/(?P<jurisdiction_slug>[\w-]+)/$', views.CatalogueForJurisdiction.as_view(),name='catalogue-jurisdiction'),
	url(r'^guides/$', views.GuidesPage.as_view()),
	url(r'^law/(?P<pk>[0-9]+)/$', views.LDPView.as_view({'get': 'get'}), name='ldp'),
    url(r'^catalogue/jurisdiction/(?P<locality>[0-9]+)/(?P<jurisdiction_slug>[\w-]+)/category/(?P<category>[0-9]+)/(?P<category_slug>[\w-]+)/$', views.CatalogueForJurisdictionForCateory.as_view(),name='catalogue-jurisdiction'),
    url(r'^law-explainers/$',views.LawExplainersPage.as_view()),
	url(r'^law-explainers/(?P<doc_id>[0-9]+)/(?P<slug>[\w-]+)/$', views.GuideIntro.as_view()),
	url(r'^write-to-us/$', views.WriteToUs.as_view()),
	url(r'^app/(?P<toc_slug>[\-a-z0-9].+)/$', views.AppPage.as_view({'get': 'list'}), name='app_page_api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
