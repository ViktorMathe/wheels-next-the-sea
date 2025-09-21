# decorators.py
from django.contrib.auth.decorators import user_passes_test

def is_superuser_or_staff(user):
    """Return True if user is superuser or staff."""
    return user.is_superuser or user.is_staff

# Global decorator
superuser_required = user_passes_test(
    is_superuser_or_staff,
    login_url='/accounts/login/'  # redirect if not authorized
)