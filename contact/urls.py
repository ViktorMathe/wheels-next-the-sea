from django.urls import path
from . import views

urlpatterns = [
    path("contact/", views.contact_page, name="contact_page"),
    path("admin/reply-contact/", views.admin_reply_contact, name="admin_reply_contact"),
]