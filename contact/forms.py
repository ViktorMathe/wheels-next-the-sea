from django import forms
from .models import ContactInfo

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ["address", "phone", "email"]