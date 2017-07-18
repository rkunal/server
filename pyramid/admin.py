from django.contrib import admin

from .models import *

from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter


admin.site.register(NyaayaApp)
admin.site.register(
    AppTOC,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'app',
        'pyramid_doc',
    ),
    list_display_links=(
        'indented_title',
    ),
    list_filter =
    (
        ('parent', TreeRelatedFieldListFilter),
    )
)

class PyramidDocAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title','is_draft')
    list_filter = ['is_draft','created_at','updated_at']

admin.site.register(PyramidDoc,PyramidDocAdmin)