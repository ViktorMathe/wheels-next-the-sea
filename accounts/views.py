# In your app, e.g., users/views.py
from allauth.account.views import ConfirmEmailView
from django.shortcuts import redirect

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        # call the original get method
        response = super().get(*args, **kwargs)
        # add your custom redirect
        return redirect('/')  # or wherever you want