from django.shortcuts import render
from rest_framework.generics import ListAPIView
from events.models import Event
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
)
from .serializers import (
	EventListSerializer,
	EventDetailSerializer,
	EventCreateUpdateSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOrganizer
from rest_framework.filters import OrderingFilter, SearchFilter
from django.utils import timezone
from django.db.models import Q


class EventListView(ListAPIView):
	now = timezone.now()
	queryset = Event.objects.filter(Q(date=now.date(),time__gt=now.today().time()) | Q(date__gt=now.date())).distinct()
	serializer_class = EventListSerializer
	permission_classes = [AllowAny,]
	filter_backends = [OrderingFilter, SearchFilter,]
	search_fields = ['name', 'description', 'organizer__username']


class EventDetailView(RetrieveAPIView):
	queryset = Event.objects.all()
	serializer_class = EventDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [AllowAny,]


class EventCreateView(CreateAPIView):
	serializer_class = EventCreateUpdateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)

class EventUpdateView(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated,IsOrganizer]


class EventDeleteView(DestroyAPIView):
	queryset = Event.objects.all()
	serializer_class = EventListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated,IsAdminUser]
