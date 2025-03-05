from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                f"New message from {form.cleaned_data['name']}",
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['admin@example.com'],  # Replace with your email
            )
            return render(request, 'contact_success.html')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
