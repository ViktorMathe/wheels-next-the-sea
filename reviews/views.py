from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

def reviews(request):
    reviews = Review.objects.order_by('-created_at')
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews')

    return render(request, 'reviews.html', {'form': form, 'reviews': reviews})
