from rest_framework import serializers

from user.serializers import CustomUserSerializer

from .models import EventModel


class EventSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = EventModel
        fields = ["title", "description", "date", "location", "owner", "attendees"]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventModel
        fields = ["title", "description", "date", "location"]

    def create(self, validated_data):
        # Set the owner field to the authenticated user
        validated_data["owner"] = self.context["request"].user

        return super().create(validated_data)
