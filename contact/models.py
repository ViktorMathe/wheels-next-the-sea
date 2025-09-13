from django.db import models

class ContactInfo(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Contact Info ({self.id})"