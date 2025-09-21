# accounts/views.py
from allauth.account.views import ConfirmEmailView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class CustomConfirmEmailView(ConfirmEmailView):
    """Confirm email, mark it verified, then redirect to login."""

    def get(self, *args, **kwargs):
        # Confirm the email
        self.object = self.get_object()
        self.object.confirm(self.request)

        # Add a message for the login page
        messages.success(self.request, "✅ Your email has been confirmed. You can now log in.")

        # Redirect to login page
        return redirect(reverse("account_login"))