from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    flyer = models.ImageField(upload_to='event_flyers/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    folder = models.ForeignKey('gallery.Folder', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def is_past_event(self):
        return self.date < timezone.now()