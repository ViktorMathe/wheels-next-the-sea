from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ContactForm, ContactInfoForm
from .models import ContactInfo, ContactNotification
import traceback
import os

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

def contact_page(request):
    contact_info, _ = ContactInfo.objects.get_or_create(id=1)

    if request.method == "POST" and "contact_submit" in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data["name"]
            email = contact_form.cleaned_data["email"]
            message = contact_form.cleaned_data["message"]

            email_success = True

            # --- Send email to admins ---
            try:
                notification = ContactNotification.objects.first()
                if notification and notification.recipients.exists():
                    recipients = [user.email for user in notification.recipients.all() if user.email]
                else:
                    recipients = [user.email for user in User.objects.filter(is_superuser=True) if user.email]

                if recipients:
                    admin_email = EmailMessage(
                        subject=f"New Contact Message from {name}",
                        body=f"From: {name} <{email}>\n\n{message}",
                        from_email=settings.EMAIL_HOST_USER,
                        to=recipients,
                        reply_to=[email],
                    )
                    admin_email.send(fail_silently=False)
                    
                    # --- Send auto-reply to sender ---
                try:
                    user_email = EmailMessage(
                        subject="Thanks for contacting Wheels Next The Sea",
                        body=(
                            f"Hello {name},\n\n"
                            "Thank you for reaching out to us. "
                            "We have received your message and will try to respond within 48 hours.\n\n"
                            "Best regards,\n"
                            "Wheels Next The Sea Team"
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        to=[email],
                        reply_to=[settings.EMAIL_HOST_USER]
                    )
                    user_email.send(fail_silently=False)
                except Exception as e:
                    email_success = False
                    if ADMIN_EMAIL:
                        error_email = EmailMessage(
                            subject="Error sending auto-reply email",
                            body=f"Error details:\n\n{traceback.format_exc()}",
                            from_email=settings.EMAIL_HOST_USER,
                            to=[ADMIN_EMAIL]
                        )
                        try:
                            error_email.send(fail_silently=True)
                        except:
                            pass
            except Exception as e:
                email_success = False
                # send email about this error to ADMIN_EMAIL
                if ADMIN_EMAIL:
                    error_email = EmailMessage(
                        subject="Error sending contact form email",
                        body=f"Error details:\n\n{traceback.format_exc()}",
                        from_email=settings.EMAIL_HOST_USER,
                        to=[ADMIN_EMAIL]
                    )
                    try:
                        error_email.send(fail_silently=True)
                    except:
                        pass

            # --- User message ---
            if email_success:
                messages.success(request, "Your message has been sent successfully!")
            else:
                messages.error(request, "There is some error, please try again later!")

            return redirect("contact_page")
    else:
        contact_form = ContactForm()

    # Superuser editing contact info
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