from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('upload/', views.upload_images, name='upload_images'),
    path('delete-image/', views.delete_image, name="delete_image"),
]
