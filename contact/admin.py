# admin.py
from django.contrib import admin
from .models import ContactNotification

@admin.register(ContactNotification)
class ContactNotificationAdmin(admin.ModelAdmin):
    filter_horizontal = ('recipients',)  # nice multi-select widget
    
    def get_recipients(self, obj):
        return ", ".join([user.email for user in obj.recipients.all()])
    get_recipients.short_description = "Recipients"