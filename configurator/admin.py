from django.contrib import admin
from .models import *
from adminsortable2.admin import SortableAdminMixin

class AppTOCExplainerMapAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

class AppTOCHomeExplainerMapAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(AppTOCExplainerMap, AppTOCExplainerMapAdmin)
admin.site.register(AppTOCHomeExplainerMap, AppTOCHomeExplainerMapAdmin)

