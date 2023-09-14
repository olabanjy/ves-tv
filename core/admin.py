from django.contrib import admin
from .models import *

from import_export import resources

from import_export.admin import ImportExportModelAdmin


# Register your models here.

class ContentResource(resources.ModelResource):

    class Meta:
        model = Content


class ContentAdmin(ImportExportModelAdmin):
    resource_classes = [ContentResource]

admin.site.register(ContentCategory)
admin.site.register(ContentGenre)
admin.site.register(Content, ContentAdmin)
admin.site.register(Episode)
admin.site.register(WatchedContent)


