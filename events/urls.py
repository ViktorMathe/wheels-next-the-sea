from django.urls import path
from . import views

urlpatterns = [
    path('current-events/', views.current_events, name='current_events'),
    path('past-events/', views.past_events, name='past_events'),
    path('manage-events/', views.manage_events, name='manage_events'),
]
