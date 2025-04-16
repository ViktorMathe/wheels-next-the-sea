from django.db import models
from django.core.files.base import ContentFile
from cloudinary.models import CloudinaryField
import os


class Folder(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class UploadImages(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='images')
    pic = CloudinaryField('images')
    uploaded_by = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)


