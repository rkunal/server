from django.shortcuts import render
from configurator.models import *
from seo.views import SeoManager
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from configurator.serializers import *
from django.db.models import Q
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from seo.views import SeoManager
from django.http import Http404

from pyramid.models import *
from .serializers import *
from seo.serializers import *
import django_filters.rest_framework
from rest_framework import viewsets, generics, serializers, authentication, permissions, status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from mptt.utils import drilldown_tree_for_node
import json

import logging
logger = logging.getLogger(__name__)

from django.db.models import Q
from lxml import etree
from cobalt.render import HTMLRenderer as CobaltHTMLRenderer



