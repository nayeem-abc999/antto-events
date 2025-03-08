from django.urls import path
from .views import event_list_create, event_detail

app_name = 'events'

urlpatterns = [
    path('v1/events/', event_list_create, name='event-list-create'),
    path('v1/events/<int:event_id>/', event_detail, name='event-detail'),
]
