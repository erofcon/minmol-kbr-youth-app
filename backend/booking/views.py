# booking/views.py
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import generics, serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import RoomSerializer, RoomTagSerializer, BookingSerializer, BookingBusySerializer
from .models import RoomTag, Room, Booking, Status
from core.auth import TelegramInitDataAuthentication
from rest_framework.permissions import IsAuthenticated


class RoomTagsView(generics.ListAPIView):
    """
    API для получения списка тегов помещений.
    """
    queryset = RoomTag.objects.all()
    serializer_class = RoomTagSerializer
    authentication_classes = [TelegramInitDataAuthentication]
    permission_classes = [IsAuthenticated]


class RoomView(generics.ListAPIView):
    """
    API для получения списка помещений.
    """
    queryset = Room.objects.prefetch_related('tags').filter(is_active=True)
    serializer_class = RoomSerializer
    authentication_classes = [TelegramInitDataAuthentication]
    permission_classes = [IsAuthenticated]


@extend_schema(
    methods=['GET'],
    summary="Получить список моих бронирований",
    description="Возвращает список бронирований текущего Telegram-пользователя (по initData). Поддерживает пагинацию.",
)
@extend_schema(
    methods=['POST'],
    summary="Создать новое бронирование",
    description="Создает новую заявку на бронирование помещения. После создания придёт уведомление в Telegram.",
)
class BookingView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.select_related('room').order_by('-start_at')
    authentication_classes = [TelegramInitDataAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tg = getattr(self.request, 'tg_init_data', {}) or {}
        user = tg.get('user') or {}
        tg_id = str(user.get('id') or '')
        if not tg_id:
            raise serializers.ValidationError({'detail': 'Telegram id не найден'})
        return self.queryset.filter(applicant_tg_id=tg_id)

    def perform_create(self, serializer):
        tg = getattr(self.request, 'tg_init_data', {}) or {}
        user = tg.get('user') or {}
        tg_id = str(user.get('id') or '')
        username = (user.get('username') or '').strip() or None
        # сигналы отправят уведомления автоматически
        serializer.save(applicant_tg_id=tg_id, applicant_tg_username=username)


@extend_schema(
    methods=['GET'],
    summary="Получить занятые слоты помещения",
    description="Возвращает интервалы, когда помещение занято подтверждёнными бронями (статус APPROVED).",
    parameters=[
        OpenApiParameter(name='start', description='Начало диапазона (ISO 8601)', required=False, type=str),
        OpenApiParameter(name='end', description='Конец диапазона (ISO 8601)', required=False, type=str),
    ]
)
class RoomBusyView(generics.ListAPIView):
    serializer_class = BookingBusySerializer
    pagination_class = None
    authentication_classes = [TelegramInitDataAuthentication]
    permission_classes = [IsAuthenticated]

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

        if start_dt and end_dt and end_dt <= start_dt:
            raise serializers.ValidationError({'detail': "Параметр 'end' должен быть позже 'start'."})

        if start_dt and end_dt:
            qs = qs.filter(start_at__lt=end_dt, end_at__gt=start_dt)
        elif start_dt:
            qs = qs.filter(end_at__gt=start_dt)
        elif end_dt:
            qs = qs.filter(start_at__lt=end_dt)
        else:
            qs = qs.filter(end_at__gt=timezone.now())

        return qs


@extend_schema(
    methods=['GET'],
    summary="Детали моей заявки",
    description="Возвращает полную информацию о заявке текущего Telegram-пользователя."
)
class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    authentication_classes = [TelegramInitDataAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tg = getattr(self.request, 'tg_init_data', {}) or {}
        user = tg.get('user') or {}
        tg_id = str(user.get('id') or '')
        return Booking.objects.select_related('room', 'room__center').filter(applicant_tg_id=tg_id)