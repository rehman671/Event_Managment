from rest_framework import viewsets

from .models import EventModel
from .serializers import EventSerializer

# Create your views here.


class EventViewset(viewsets.ModelViewSet):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
