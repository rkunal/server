from django.contrib import admin
from .models import *

class StaticSeoAdmin(admin.ModelAdmin):
    search_fields = ['url','title']
    list_display = ('url','title','created_at','updated_at')
    list_filter = ['is_deleted','created_at','updated_at']


admin.site.register(StaticSeo, StaticSeoAdmin)
