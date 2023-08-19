from rest_framework import viewsets

from .models import EventModel
from .permissions import CustomPermission
from .serializers import EventSerializer

# Create your views here.


class EventViewset(viewsets.ModelViewSet):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    permission_classes = [CustomPermission]
