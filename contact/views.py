from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import ContactForm, ContactInfoForm
from .models import ContactInfo

def contact_page(request):
    # Get contact info (or create default one)
    contact_info, _ = ContactInfo.objects.get_or_create(id=1)

    # Handle contact form (sends email)
    if request.method == "POST" and "contact_submit" in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data["name"]
            email = contact_form.cleaned_data["email"]
            message = contact_form.cleaned_data["message"]

            # Get superuser email
            superuser = User.objects.filter(is_superuser=True).first()
            if superuser and superuser.email:
                send_mail(
                    subject=f"New Contact Message from {name}",
                    message=f"From: {name} <{email}>\n\n{message}",
                    from_email=email,
                    recipient_list=[superuser.email],
                )
            return redirect("contact_page")

    else:
        contact_form = ContactForm()

    # Handle superuser editing ContactInfo
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