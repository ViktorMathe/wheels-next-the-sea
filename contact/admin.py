# admin.py
from django.contrib import admin
from .models import ContactNotification

@admin.register(ContactNotification)
class ContactNotificationAdmin(admin.ModelAdmin):
    filter_horizontal = ('recipients',)  # nice multi-select widget