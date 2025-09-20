import traceback
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render
import os

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

class ExceptionEmailMiddleware:
    """
    Catches all unhandled exceptions, sends an email to ADMIN_EMAIL,
    and shows a friendly error page to the user.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # Compose the email
            subject = f"Error on site: {request.path}"
            body = (
                f"Exception Type: {type(e).__name__}\n"
                f"Exception: {e}\n\n"
                f"Path: {request.path}\n"
                f"Method: {request.method}\n"
                f"User: {request.user if hasattr(request, 'user') else 'Anonymous'}\n\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
            if ADMIN_EMAIL:
                try:
                    email = EmailMessage(
                        subject=subject,
                        body=body,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[ADMIN_EMAIL],
                    )
                    email.send(fail_silently=True)
                except Exception as mail_err:
                    print(f"Failed to send error email: {mail_err}")

            # Render a friendly error page with "Go Back" button
            return render(request, "error_page.html", {
                "message": "Oops! Something went wrong. Please contact the site admin.",
                "back_url": request.META.get("HTTP_REFERER", "/")
            }, status=500)