from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import RoomSerializer, RoomTagSerializer, BookingSerializer
from .models import RoomTag, Room, Booking


class RoomTagsView(APIView):

    @classmethod
    def get(cls, request):
        tags = RoomTag.objects.all()
        serializer = RoomTagSerializer(tags, many=True)
        return Response(serializer.data)


class RoomView(APIView):

    @classmethod
    def get(cls, request):
        rooms = Room.objects.prefetch_related('tags').filter(is_active=True)

        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class BookingView(APIView):
    """
    API для получения списка своих бронирований и создания новых.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(name='tg_username', description='Telegram username для фильтрации бронирований',
                             required=True, type=str)
        ],
        responses=BookingSerializer(many=True)
    )
    def get(self, request):
        """
        Возвращает список бронирований для пользователя Telegram.
        Требуется query-параметр: ?tg_username=some_username
        """

        tg_username = request.query_params.get('tg_username')

        if not tg_username:
            return Response(
                {"error": "Параметр 'tg_username' является обязательным."},
                status=status.HTTP_400_BAD_REQUEST
            )

        bookings = Booking.objects.filter(
            applicant_tg_username=tg_username
        ).select_related('room').order_by('-start_at')

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=BookingSerializer,
        responses={201: BookingSerializer}
    )
    def post(self, request):
        """
        Создает новую заявку на бронирование.
        """
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
