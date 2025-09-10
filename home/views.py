from django.shortcuts import render, redirect
from reviews.models import Review
from .models import AboutUs
from .forms import AboutUsForm
from events.models import Event
from django.utils import timezone

# Create your views here.
def home(request):
    reviews = Review.objects.order_by('-created_at')[:10]  # Limit to latest 10
    about, created = AboutUs.objects.get_or_create(id=1)
    next_event = Event.objects.filter(date__gte=timezone.now()).order_by('date').first()
    if request.user.is_superuser and request.method == "POST":
        form = AboutUsForm(request.POST, instance=about)
        if form.is_valid():
            form.save()
            return redirect("home")  # reloads same page
    else:
        form = AboutUsForm(instance=about)
    context = {'reviews':reviews, "about": about, "form": form, "next_event": next_event}
    return render(request, 'index.html', context)
