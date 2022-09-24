from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(WebhookBackup)
admin.site.register(Subscribtion)


admin.site.register(UserProfile)
admin.site.register(UserSubscribtion)
