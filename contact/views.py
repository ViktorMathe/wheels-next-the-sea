from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .forms import ContactForm, ContactInfoForm
from .models import ContactInfo, ContactNotification

def contact_page(request):
    contact_info, _ = ContactInfo.objects.get_or_create(id=1)

    if request.method == "POST" and "contact_submit" in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data["name"]
            email = contact_form.cleaned_data["email"]
            message = contact_form.cleaned_data["message"]

            # Get chosen notification recipients or fallback to all superusers
            notification = ContactNotification.objects.first()
            if notification and notification.recipients.exists():
                recipients = [user.email for user in notification.recipients.all() if user.email]
            else:
                recipients = [user.email for user in User.objects.filter(is_superuser=True) if user.email]

            if recipients:
                # 1) Send one email with BCC to admins
                admin_email = EmailMessage(
                    subject=f"New Contact Message from {name}",
                    body=f"From: {name} <{email}>\n\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],  # just your site address in "To"
                    bcc=recipients,  # all admins hidden here
                    reply_to=[email],
                )
                admin_email.send()

                # 2) Auto-reply to sender
                user_email = EmailMessage(
                    subject="Thanks for contacting Wheels Next The Sea",
                    body=(
                        f"Hello {name},\n\n"
                        "Thank you for reaching out to us. "
                        "We have received your message and will try to respond within 48 hours.\n\n"
                        "Best regards,\n"
                        "Wheels Next The Sea Team"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                user_email.send()

            return redirect("contact_page")
    else:
        contact_form = ContactForm()

    # Superuser editing contact info
    if request.method == "POST" and "info_submit" in request.POST and request.user.is_superuser:
        info_form = ContactInfoForm(request.POST, instance=contact_info)
        if info_form.is_valid():
            info_form.save()
            return redirect("contact_page")
    else:
        info_form = ContactInfoForm(instance=contact_info)

    return render(request, "contact.html", {
        "contact_form": contact_form,
        "info_form": info_form,
        "contact_info": contact_info,
    })