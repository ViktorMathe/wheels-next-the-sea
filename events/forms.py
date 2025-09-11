from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",  # HTML5 date-time picker
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = Event
        fields = ["title", "description", "date", "flyer"]