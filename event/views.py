from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def attend(self, request, pk=None):
        try:
            event = EventModel.objects.get(eid=pk)
        except EventModel.DoesNotExist:
            return Response({"message": "Event Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        user = self.request.user
        event.attendees.add(user)
        return Response({"message": "Event Attended"}, status=status.HTTP_200_OK)
