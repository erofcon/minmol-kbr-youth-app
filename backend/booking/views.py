from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializers import RoomSerializer, RoomTagSerializer, BookingSerializer, \
    BookingBusySerializer
from .models import RoomTag, Room, Booking, Status
from rest_framework import serializers


class RoomTagsView(generics.ListAPIView):
    """
    API для получения списка тегов помещении.
    """
    queryset = RoomTag.objects.all()
    serializer_class = RoomTagSerializer


class RoomView(generics.ListAPIView):
    """
    API для получения списка помещении.
    """
    queryset = Room.objects.prefetch_related('tags').filter(is_active=True)
    serializer_class = RoomSerializer


@extend_schema(
    methods=['GET'],  # Этот декоратор только для GET
    summary="Получить список своих бронирований",
    description="Возвращает список бронирований для указанного пользователя Telegram. Поддерживает пагинацию.",
    parameters=[
        OpenApiParameter(
            name='tg_username',
            description='Telegram username для фильтрации бронирований',
            required=True,  # <--- Теперь это будет работать
            type=str
        )
    ]
)
@extend_schema(
    methods=['POST'],  # Этот декоратор только для POST
    summary="Создать новое бронирование",
    description="Создает новую заявку на бронирование помещения.",
)
class BookingView(generics.ListCreateAPIView):
    """
    API для получения списка своих бронирований и создания новых.
    - GET: Возвращает список бронирований для пользователя Telegram.
    - POST: Создает новую заявку на бронирование.
    """
    serializer_class = BookingSerializer
    queryset = Booking.objects.select_related('room').order_by('-start_at')

    def get_queryset(self):
        """
        Фильтрует queryset и проверяет наличие обязательного параметра.
        """
        tg_username = self.request.query_params.get('tg_username')

        if not tg_username:
            raise serializers.ValidationError(
                {'error': "Параметр 'tg_username' является обязательным."}
            )

        return self.queryset.filter(applicant_tg_username=tg_username)


@extend_schema(
    methods=['GET'],
    summary="Получить занятые слоты помещения",
    description="Возвращает интервалы, когда помещение занято. По умолчанию занятость — это статусы PENDING и APPROVED.",
    parameters=[
        OpenApiParameter(name='start',
                         description='Начало диапазона (ISO 8601)',
                         required=False, type=str),
        OpenApiParameter(name='end', description='Конец диапазона (ISO 8601)',
                         required=False, type=str),
    ]
)
class RoomBusyView(generics.ListAPIView):
    serializer_class = BookingBusySerializer
    pagination_class = None

    def _make_aware(self, dt):
        if dt and timezone.is_naive(dt):
            return timezone.make_aware(dt, timezone.get_default_timezone())
        return dt

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        qs = Booking.objects.filter(
            room_id=room_id,
            status__in=[Status.APPROVED],
        ).order_by('start_at')

        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        start_dt = self._make_aware(parse_datetime(start)) if start else None
        end_dt = self._make_aware(parse_datetime(end)) if end else None

        # Валидация диапазона
        if start_dt and end_dt and end_dt <= start_dt:
            raise serializers.ValidationError(
                {'detail': "Параметр 'end' должен быть позже 'start'."})

        if start_dt and end_dt:
            qs = qs.filter(start_at__lt=end_dt, end_at__gt=start_dt)
        elif start_dt:
            qs = qs.filter(end_at__gt=start_dt)
        elif end_dt:
            qs = qs.filter(start_at__lt=end_dt)
        else:
            qs = qs.filter(end_at__gt=timezone.now())

        return qs
