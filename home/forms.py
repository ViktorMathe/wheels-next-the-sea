from django import forms
from .models import AboutUs
from django_ckeditor_5.widgets import CKEditor5Widget

class AboutUsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = AboutUs
        fields = ['content']