from rest_framework import viewsets

from .models import EventModel
from .permissions import CustomPermission, IsEventOwner
from .serializers import EventSerializer, PostSerializer


class EventViewset(viewsets.ModelViewSet):
    queryset = EventModel.objects.all()
    permission_classes = [CustomPermission, IsEventOwner]

    def get_serializer_class(self):
        if self.action == "list":
            return EventSerializer
        elif self.action in ["create", "update"]:
            return PostSerializer
        return EventSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
