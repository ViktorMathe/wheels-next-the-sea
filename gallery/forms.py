from django import forms
from cloudinary.forms import CloudinaryFileField, CloudinaryJsFileField
from .models import Folder, UploadImages

class FolderForm(forms.ModelForm):
    name = forms.CharField()
    class Meta:
        model = Folder
        fields = ['name']


class GalleryImageForm(forms.ModelForm):
    images = forms.FileField()
    folder = forms.ModelChoiceField(queryset=Folder.objects.all())
    class Meta:
        model = UploadImages
        fields = ['images', 'folder']
