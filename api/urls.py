from django.urls import path
from api.views import (
    EventListView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
    EventCreateView,
)

urlpatterns = [
 
    path('api/list/', EventListView.as_view(), name='api-list'),
    path('api/create/', EventCreateView.as_view(), name='api-create'),
    path('api/<int:event_id>/detail/', EventDetailView.as_view(), name='api-detail'),
    path('api/<int:event_id>/update/', EventUpdateView.as_view(), name='api-update'),
    path('api/<int:event_id>/delete/', EventDeleteView.as_view(), name='api-delete'),
]