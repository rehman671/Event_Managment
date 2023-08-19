from rest_framework import serializers

from .models import EventModel


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventModel
        fields = ["title", "description", "date", "location", "owner", "attendees"]
