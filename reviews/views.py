from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm

def reviews(request):
    all_reviews = Review.objects.order_by('-created_at')
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews')
    context = {'form': form, 'all_reviews': all_reviews}
    return render(request, 'reviews.html', context)



def review_detail(request, review_id, slug):
    review = get_object_or_404(Review, id=review_id, slug=slug)
    return render(request, 'review_detail.html', {'review': review})