from django.urls import path
from . import views

urlpatterns = [
    path("", views.contact_page, name="contact_page"),
    path("reply/", views.admin_reply_contact, name="admin_reply_contact"),
]