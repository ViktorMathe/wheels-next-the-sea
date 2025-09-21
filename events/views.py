from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from wheels_next_to_sea.decorators import superuser_required
from django.utils import timezone
from .models import Event
from .forms import EventForm


@login_required
@superuser_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == "POST":
        event.delete()
        messages.success(request, f"Event '{event.title}' has been deleted successfully.")
        return redirect("events_list")  # Replace with your events list view name
    
    return render(request, "events/confirm_delete.html", {"event": event})

def current_events(request):
    next_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'current_events.html', {'next_events': next_events})

def past_events(request):
    past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    return render(request, 'past_events.html', {'past_events': past_events})


@superuser_required
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
