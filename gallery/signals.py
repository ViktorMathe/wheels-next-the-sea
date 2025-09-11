from django.db.models.signals import post_delete
from django.dispatch import receiver
import cloudinary.uploader
from .models import UploadImages, Folder
import os

# When an UploadImages object is deleted, remove it from Cloudinary
@receiver(post_delete, sender=UploadImages)
def delete_image_from_cloudinary(sender, instance, **kwargs):
    if instance.url:
        # Extract everything after '/upload/' in the URL
        path = instance.url.split("/upload/")[1]
        public_id = os.path.splitext(path)[0]  # remove file extension
        try:
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            print(f"Error deleting image from Cloudinary: {e}")


# When a Folder is deleted, remove all its images from Cloudinary

@receiver(post_delete, sender=Folder)
def delete_folder_images_from_cloudinary(sender, instance, **kwargs):
    for image in instance.images.all():
        if image.url:
            # Extract public_id from the URL
            path = image.url.split("/upload/")[1]
            public_id = os.path.splitext(path)[0]  # remove file extension
            try:
                cloudinary.uploader.destroy(public_id)
            except Exception as e:
                print(f"Error deleting image from Cloudinary: {e}")