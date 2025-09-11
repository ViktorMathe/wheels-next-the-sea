from django.db.models.signals import post_delete
from django.dispatch import receiver
import cloudinary.uploader
from .models import UploadImages, Folder


# When an UploadImages object is deleted, remove it from Cloudinary
@receiver(post_delete, sender=UploadImages)
def delete_image_from_cloudinary(sender, instance, **kwargs):
    if instance.url:
        cloudinary.uploader.destroy(instance.url.public_id)


# When a Folder is deleted, remove all its images from Cloudinary
@receiver(post_delete, sender=Folder)
def delete_folder_images_from_cloudinary(sender, instance, **kwargs):
    for image in instance.images.all():
        if image.url:
            cloudinary.uploader.destroy(image.url.public_id)