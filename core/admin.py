from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(ContentCategory)
admin.site.register(ContentGenre)
admin.site.register(Content)
admin.site.register(Episode)
admin.site.register(WatchedContent)