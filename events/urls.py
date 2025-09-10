from django.urls import path
from . import views

urlpatterns = [
    path('current-events/', views.current_events, name='current_events'),
    path('past-events/', views.past_events, name='past_events'),
    path('add-event/', views.manage_events, name='add_event'),
    path('manage-events/<int:event_id>/', views.manage_events, name='manage_events_edit'), 
]
