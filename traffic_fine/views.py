from django.shortcuts import render
from traffic_fine.serializers import *
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from lxml import etree
from cobalt.render import HTMLRenderer as CobaltHTMLRenderer
from rest_framework import viewsets, generics, serializers, authentication, permissions, status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.

class TrafficFinePagination(PageNumberPagination):
    page_size = 100

class TrafficFineViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset = TrafficFine.objects.all()
        city = self.request.query_params.get('city', '7')
        category = self.request.query_params.get('category', None)
        queryset = queryset.filter(
            Q(city_id=city) | Q(city_id=7)
        ).order_by('-city__order','order')
        if category is not None:
            queryset = queryset.filter(category_id=category)
        return queryset
    serializer_class = TrafficFineSerializer
    pagination_class = TrafficFinePagination
