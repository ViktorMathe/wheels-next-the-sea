# admin.py
from django.contrib import admin
from .models import ContactNotification


@admin.register(ContactNotification)
class ContactNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_recipients')

    def get_recipients(self, obj):
        return ", ".join([user.email for user in obj.recipients.all()])
    get_recipients.short_description = "Recipients"