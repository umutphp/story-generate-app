from django.db import models
from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget


class Story(models.Model):
    title = models.CharField(max_length=256, null=False)
    text = models.TextField(null=False)
    city = models.CharField(max_length=256, null=True)
    area = models.CharField(max_length=256, null=True)
    accented = models.BooleanField(null=True)
    language = models.CharField(max_length=5, default='tr')
    generated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.id}) / {self.city} / {self.area}"


class StoryTrigger(models.Model):
    language = models.CharField(max_length=5, default='tr')
    place = models.CharField(max_length=256, null=False)
    topic = models.CharField(max_length=256, null=False)
    characters = models.JSONField()


@admin.action(description="Mark selected stories as accented")
def make_accented(modeladmin, request, queryset):
    queryset.update(accented=True)


@admin.action(description="Mark selected stories as not-accented")
def make_not_accented(modeladmin, request, queryset):
    queryset.update(accented=True)


class StoryAdmin(admin.ModelAdmin):
    fields = ["title", "text", "city", "area", 'accented', 'language']
    list_display = ["title", "short_text", "language", "city", "area", 'accented']
    list_filter = ["language", "city", "area", "accented"]
    ordering = ["id"]
    actions = [make_accented, make_not_accented]

    def short_text(self, instance):
        return instance.text[:255] + "..."


class StoryTriggerAdmin(admin.ModelAdmin):
    fields = ["topic", "place", "language", "characters"]
    list_display = ["topic", "place", "language"]
    list_filter = ["language"]
    ordering = ["id"]

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
