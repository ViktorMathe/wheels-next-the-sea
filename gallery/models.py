from django.db import models
from django.core.files.base import ContentFile
from cloudinary.models import CloudinaryField
import os


class Folder(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class UploadImages(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    folder = models.ForeignKey(Folder, related_name="images", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=255)
    class Meta:
        unique_together = ('title', 'folder')


