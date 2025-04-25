from django import forms
from cloudinary.forms import CloudinaryFileField, CloudinaryJsFileField
from .models import Folder, UploadImages

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class FolderForm(forms.ModelForm):
    name = forms.CharField()
    class Meta:
        model = Folder
        fields = ['name']


class GalleryImageForm(forms.Form):
    images = MultipleFileField()
    class Meta:
        model = UploadImages
        fields = ['images', 'folder']

