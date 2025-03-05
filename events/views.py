from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .models import Event
from .forms import EventForm

def current_events(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'current_events.html', {'events': events})

def past_events(request):
    events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    return render(request, 'past_events.html', {'events': events})

# Restrict event management to superusers only
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def manage_events(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('current_events')
    else:
        form = EventForm()
    return render(request, 'manage_events.html', {'form': form})
