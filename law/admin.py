from django.contrib import admin
from .models import *

# Register your models here.
class WebDocAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'short_title', 'category','locality')
    search_fields = ('document_id','short_title','locality',)
    list_filter = ('locality_id',)

class WebDocXmlDataAdmin(admin.ModelAdmin):
    pass

class DocExplainerBlockAdmin(admin.ModelAdmin):
    pass

admin.site.register(WebDoc, WebDocAdmin)
admin.site.register(WebDocXmlData,WebDocXmlDataAdmin)
admin.site.register(DocExplainerBlock, DocExplainerBlockAdmin)
