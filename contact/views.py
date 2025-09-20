from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import ContactForm, ContactInfoForm
from .models import ContactInfo, ContactNotification
import traceback
import logging
import os


logger = logging.getLogger(__name__) 

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

<<<<<<< HEAD
# --- Helper function ---
def send_email_message(subject, body, to, from_email=None, reply_to=None):
=======
def send_email_message(subject, body, to, reply_to=None):
    """Send an email with a fresh SMTP connection and detailed logging."""
>>>>>>> cdc6d59 (Added more security)
    try:
        connection = get_connection(fail_silently=False)
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email if from_email else settings.EMAIL_HOST_USER,
            to=to,
            reply_to=reply_to or []
        )
        email.connection = connection
        email.send()
        logger.info(f"Email sent successfully: subject='{subject}', to={to}")
        return True
<<<<<<< HEAD
    except Exception:
=======
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Error sending email: subject='{subject}', to={to}\n{error_details}")
>>>>>>> cdc6d59 (Added more security)
        if ADMIN_EMAIL:
            try:
                error_email = EmailMessage(
                    subject="Email sending error",
                    body=f"Error details:\n\n{error_details}",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[ADMIN_EMAIL],
                )
                error_email.send(fail_silently=True)
            except Exception as inner_e:
                logger.error(f"Failed to send error report email to ADMIN_EMAIL: {inner_e}")
        return False


def contact_page(request):
    contact_info, _ = ContactInfo.objects.get_or_create(id=1)

    if request.method == "POST" and "contact_submit" in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data["name"]
            email = contact_form.cleaned_data["email"]
            message = contact_form.cleaned_data["message"]

<<<<<<< HEAD
            # --- Send admin notification ---
=======
            # --- Admin notification ---
>>>>>>> cdc6d59 (Added more security)
            notification = ContactNotification.objects.first()
            recipients = (
                [user.email for user in notification.recipients.all() if user.email]
                if notification and notification.recipients.exists()
                else [user.email for user in User.objects.filter(is_superuser=True) if user.email]
            )

            admin_sent = send_email_message(
                subject=f"New Contact Message from {name}",
                body=f"From: {name} <{email}>\n\n{message}",
                to=recipients,
<<<<<<< HEAD
                from_email=settings.EMAIL_HOST_USER,  # must match your verified SMTP email
                reply_to=[email]  # reply will go to the user
            )

            # --- Send auto-reply to user (Gmail-safe) ---
=======
                reply_to=[email],
            )

            # --- Auto-reply to user ---
>>>>>>> cdc6d59 (Added more security)
            user_sent = send_email_message(
                subject="Thanks for contacting Wheels Next The Sea",
                body=(
                    f"Hello {name},\n\n"
                    "Thank you for reaching out to us. We have received your message "
                    "and will try to respond within 48 hours.\n\nBest regards,\nWheels Next The Sea Team"
                ),
                to=[email],
<<<<<<< HEAD
                from_email=settings.EMAIL_HOST_USER,  # MUST match your SMTP verified email
                reply_to=[settings.EMAIL_HOST_USER]   # reply-to points to your site email
=======
                reply_to=[settings.EMAIL_HOST_USER],
>>>>>>> cdc6d59 (Added more security)
            )

            if admin_sent and user_sent:
                messages.success(request, "Your message has been sent successfully!")
            else:
                messages.error(request, "There was an error sending your message. Please try again later.")

            return redirect("contact_page")
    else:
        contact_form = ContactForm()

    # --- Superuser contact info edit ---
    if request.method == "POST" and "info_submit" in request.POST and request.user.is_superuser:
        info_form = ContactInfoForm(request.POST, instance=contact_info)
        if info_form.is_valid():
            info_form.save()
            messages.success(request, "Contact information updated successfully.")
            return redirect("contact_page")
    else:
        info_form = ContactInfoForm(instance=contact_info)

    return render(request, "contact.html", {
        "contact_form": contact_form,
        "info_form": info_form,
        "contact_info": contact_info,
    })