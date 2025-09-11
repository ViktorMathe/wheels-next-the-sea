from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "created_by", "is_past_event")
    list_filter = ("date", "created_by")
    search_fields = ("title", "description")
    ordering = ("-date",)