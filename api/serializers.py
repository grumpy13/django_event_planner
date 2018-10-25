from rest_framework import serializers
from events.models import Event

class EventListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )

    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )

    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
   
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'date',
            'time',
            'seats',
            'detail',
            'update',
            'delete',
            ]

#     organizer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
class EventDetailSerializer(serializers.ModelSerializer):

    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )

    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "event_id"
        )
    
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'location',
            'date',
            'time',
            'seats',
            'organizer',
            'update',
            'delete',
            ]

class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'date',
            'time',
            'seats',
            ]