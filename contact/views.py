from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from .forms import ContactForm, ContactInfoForm
from .models import ContactInfo, ContactNotification
from django.core.signing import Signer, BadSignature
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html, escape
import traceback
import logging
import os

logger = logging.getLogger(__name__)
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

# --- Helper function ---
def send_email_message(subject, body, to, from_email=None, reply_to=None, html=False):
    """Send an email with optional HTML content."""
    try:
        connection = get_connection(fail_silently=False)
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email if from_email else settings.EMAIL_HOST_USER,
            to=to,
            reply_to=reply_to or []
        )
        if html:
            email.content_subtype = "html"  # Send HTML email
        email.connection = connection
        email.send()
        logger.info(f"Email sent successfully: subject='{subject}', to={to}")
        return True
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Error sending email: subject='{subject}', to={to}\n{error_details}")
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

            # --- Admin notification ---
            notification = ContactNotification.objects.first()
            recipients = (
                [user.email for user in notification.recipients.all() if user.email]
                if notification and notification.recipients.exists()
                else [user.email for user in User.objects.filter(is_superuser=True) if user.email]
            )

            signer = Signer()
            reply_links_html = ""
            for user in User.objects.filter(email__in=recipients, is_superuser=True):
                contact_token = signer.sign(f"{email}:{name}:{message}")
                # Build the reply link (include token)
                reply_url = request.build_absolute_uri(
                    reverse("admin_reply_contact") + "?" + urlencode({"token": contact_token})
                )
                reply_links_html += f"""
                    <tr>
                        <td align="center" style="padding: 10px 0;">
                            <a href="{reply_url}" target="_blank" 
                               style="
                                    display: inline-block;
                                    padding: 12px 24px;
                                    background-color: #1E40AF;
                                    color: #ffffff;
                                    text-decoration: none;
                                    border-radius: 6px;
                                    font-weight: bold;
                                    font-family: Arial, sans-serif;
                               ">
                               Reply to {escape(name)}
                            </a>
                        </td>
                    </tr>
                """
            
            # Construct full HTML email
            admin_body_html = f"""
            <html>
              <body style="font-family: Arial, sans-serif; color: #111; line-height: 1.5;">
                <h2>New Contact Message Received</h2>
                <p><strong>From:</strong> {escape(name)} &lt;{escape(email)}&gt;</p>
                <p><strong>Message:</strong></p>
                <p>{escape(message)}</p>
                <hr style="border: 1px solid #ccc;">
                <h3>Reply via site:</h3>
                <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                    {reply_links_html}
                </table>
                <p style="color:#555; font-size: 12px;">This email is sent automatically. Only intended recipients (superusers) can use the links.</p>
              </body>
            </html>
            """
            
            # Send HTML email
            admin_sent = send_email_message(
                subject=f"New Contact Message from {name}",
                body=admin_body_html,
                to=recipients,
                from_email=settings.EMAIL_HOST_USER,
                reply_to=[email],
                html=True
            )

            # --- Auto-reply to user ---
            user_sent = send_email_message(
                subject="Thanks for contacting Wheels Next The Sea",
                body=(
                    f"Hello {name},\n\n"
                    "Thank you for reaching out to us. We have received your message "
                    "and will try to respond within 48 hours.\n\nBest regards,\nWheels Next The Sea Team"
                ),
                to=[email],
                from_email=settings.EMAIL_HOST_USER,
                reply_to=[settings.EMAIL_HOST_USER]
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


@login_required(login_url='/accounts/login/')
def admin_reply_contact(request):
    token = request.GET.get("token")
    signer = Signer()

    try:
        contact_email, contact_name, original_message = signer.unsign(token).split(":", 2)
    except BadSignature:
        messages.error(request, "Invalid reply link.")
        return redirect("contact_page")

    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to reply.")
        return redirect("contact_page")

    if request.method == "POST":
        reply_message = request.POST.get("reply_message")
        footer_html = f"""
                <hr style="border: 1px solid #ccc; margin: 20px 0;">
                <p style="font-size: 13px; color: #555;">
                    Wheels Next The Sea<br>
                    Website: <a href="https://wheelsnextthesea.co.uk" style="color: #1E40AF; text-decoration: none;">www.wheelsnextthesea.co.uk</a><br>
                    Email: <a href="mailto:{settings.EMAIL_HOST_USER}" style="color: #1E40AF; text-decoration: none;">{settings.EMAIL_HOST_USER}</a><br>
                    Thank you for contacting us. We appreciate your message.
                </p>
                """
        
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #111; line-height: 1.5;">
            <p>{escape(reply_message)}</p>
            {footer_html}
        </body>
        </html>
        """

        reply_sent = send_email_message(
                subject=f"Reply from Wheels Next The Sea",
                body=email_body,
                to=[contact_email],
                from_email=settings.EMAIL_HOST_USER,
                reply_to=[settings.EMAIL_HOST_USER],
                html=True
            )
        if reply_sent :
            messages.success(request, f"Reply sent to {contact_name} ({contact_email})!")
        else:
            messages.error(request, "There was an error sending your message. Please try again later.")
        return redirect("contact_page")

    return render(request, "admin_reply_contact.html", {
        "contact_name": contact_name,
        "contact_email": contact_email,
        "original_message": original_message,
    })