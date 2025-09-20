from django.db import models
from django.contrib.auth.models import User

class ContactInfo(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Contact Info ({self.id})"

class ContactNotification(models.Model):
    recipients = models.ManyToManyField(
        User,
        limit_choices_to={'is_superuser': True},
        help_text="Choose which superusers should receive contact form emails."
    )

    def __str__(self):
        return "Contact Form Notification Settings"