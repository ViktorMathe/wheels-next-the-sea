from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<str:folder_name>', views.year_gallery, name="year_gallery"),
    path('upload/', views.upload_images, name='upload_images'),
    path('delete-image/', views.delete_image, name="delete_image"),
    path('delete-multiple-images/', views.delete_multiple_images, name='delete_multiple_images'),
    path('delete-folder/', views.delete_folder, name='delete_folder'),
]
