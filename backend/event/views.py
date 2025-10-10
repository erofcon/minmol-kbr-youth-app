from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event
from .serializers import EventListSerializer


class EventListView(APIView):

    @classmethod
    def get(cls, request):
        events = Event.objects.all()
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
