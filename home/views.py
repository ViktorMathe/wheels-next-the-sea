from django.shortcuts import render
from reviews.models import Review

# Create your views here.
def home(request):
    reviews = Review.objects.order_by('-created_at')[:10]  # Limit to latest 10
    context = {'reviews':reviews}
    return render(request, 'index.html', context)