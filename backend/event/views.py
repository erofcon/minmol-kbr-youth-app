from rest_framework import generics
from .models import Event
from .serializers import EventListSerializer


class EventListView(generics.ListAPIView):
    """
    API для получения списка мероприятии
    """
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
