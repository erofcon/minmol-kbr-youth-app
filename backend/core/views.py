from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .auth import TelegramInitDataAuthentication


@extend_schema(
    tags=["System"],
    summary="Проверка доступности и Telegram-авторизации",
    description="Возвращает ok, серверное время и информацию о Telegram-пользователе по подписанному initData."
)
class HealthView(APIView):
    authentication_classes = [TelegramInitDataAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tg = getattr(request, 'tg_init_data', {}) or {}
        tg_user = tg.get('user') or {}

        return Response({
            "ok": True,
            "server_time": timezone.now().isoformat(),
            "user": {
                "id": tg_user.get("id"),
                "username": tg_user.get("username"),
                "first_name": tg_user.get("first_name"),
                "last_name": tg_user.get("last_name"),
                "language_code": tg_user.get("language_code"),
                "is_premium": tg_user.get("is_premium"),
            }
        })
