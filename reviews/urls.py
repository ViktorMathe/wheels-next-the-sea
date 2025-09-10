from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews, name="reviews"),
    path('reviews/<int:review_id>/<slug:slug>/', views.review_detail, name='review_detail')
]