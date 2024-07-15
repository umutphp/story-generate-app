import functools

from django.db import models
from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget


class StoryTrigger(models.Model):
    language = models.CharField(max_length=5, default="tr")
    place = models.CharField(max_length=256, null=False)
    topic = models.CharField(max_length=256, null=False)
    setting = models.JSONField()

    @property
    def setting_str_for_prompt(self):
        return f"* Place: {self.place}\n* Topic: {self.topic}\n* Characters: {self.characters}\n"

    @property
    def characters(self):
        characters = ""

        for char in self.setting["characters"]:
            characters += char["kind"].lower() + " with name " + char["name"] + ", "

        return characters

    def __str__(self):
        return f"{self.topic} ({self.id}) / {self.language} / {self.place}"


class Story(models.Model):
    title = models.CharField(max_length=256, null=False)
    text = models.TextField(null=False)
    city = models.CharField(max_length=256, blank=True, default="")
    area = models.CharField(max_length=256, blank=True, default="")
    accented = models.BooleanField(null=True)
    language = models.CharField(max_length=5, default="tr")
    generated = models.BooleanField(default=False)
    story_trigger = models.ForeignKey(
        StoryTrigger, on_delete=models.CASCADE, default=None, null=True
    )

    def __str__(self):
        return f"{self.title} ({self.id}) / {self.city} / {self.area}"


@admin.action(description="Mark selected stories as accented")
def make_accented(modeladmin, request, queryset):
    queryset.update(accented=True)


@admin.action(description="Mark selected stories as not-accented")
def make_not_accented(modeladmin, request, queryset):
    queryset.update(accented=True)


class StoryAdmin(admin.ModelAdmin):
    fields = ["title", "text", "city", "area", "accented", "language", "story_trigger"]
    list_display = ["title", "short_text", "language", "story_trigger", "accented"]
    list_filter = ["language", "accented"]
    ordering = ["-id"]
    actions = [make_accented, make_not_accented]

    def short_text(self, instance):
        return instance.text[:255] + "..."


class StoryTriggerAdmin(admin.ModelAdmin):
    fields = ["topic", "place", "language", "setting"]
    list_display = ["topic", "place", "language"]
    list_filter = ["language"]
    ordering = ["-id"]

    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }
