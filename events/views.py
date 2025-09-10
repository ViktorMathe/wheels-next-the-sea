from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .models import Event
from .forms import EventForm

def current_events(request):
    next_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'current_events.html', {'next_events': next_events})

def past_events(request):
    past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    return render(request, 'past_events.html', {'past_events': past_events})

# Restrict event management to superusers only
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def manage_events(request, event_id=None):
    if event_id:
        event = Event.objects.get(id=event_id)
    else:
        event = None
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.created_by = request.user
            new_event.save()
            return redirect('current_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'manage_events.html', {'form': form})
