from django.contrib import admin
from core import models


# Register your models here.

admin.site.register(models.Story, models.StoryAdmin)
admin.site.register(models.StoryTrigger, models.StoryTriggerAdmin)
