from django.contrib import admin
from .models import Folder, UploadImages

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(UploadImages)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'folder', 'uploaded_by', 'uploaded_at', 'url')