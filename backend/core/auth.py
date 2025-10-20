import time
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .telegram import verify_init_data


class TelegramAuthUser:

    def __init__(self, tg_id: str, username: str = "", first_name: str = "", last_name: str = ""):
        self.tg_id = str(tg_id)
        self.username = f"tg_{self.tg_id}"
        self.first_name = first_name or ""
        self.last_name = last_name or ""
        self.is_staff = False
        self.is_superuser = False

    @property
    def is_authenticated(self):
        return True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username


class TelegramInitDataAuthentication(BaseAuthentication):
    """
    Аутентифицирует по Telegram initData без создания локального пользователя.
    Достаёт initData из:
    - заголовка X-Telegram-Init-Data
    - query-параметра init_data
    - тела запроса (form/json) по ключу init_data
    """
    header_name = 'HTTP_X_TELEGRAM_INIT_DATA'

    def authenticate(self, request):
        init_data = (
                request.META.get(self.header_name)
                or request.query_params.get('init_data')
                or (request.data.get('init_data') if hasattr(request, 'data') else None)
        )

        if not init_data:
            return None

        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if not bot_token:
            raise AuthenticationFailed('Telegram bot token not configured')

        try:
            data = verify_init_data(init_data, bot_token)
        except Exception:
            raise AuthenticationFailed('Invalid Telegram init data')

        max_age = int(getattr(settings, 'TELEGRAM_INIT_DATA_TTL', 86400))
        try:
            auth_date = int(data.get('auth_date', '0'))
        except ValueError:
            auth_date = 0
        if not auth_date or (time.time() - auth_date) > max_age:
            raise AuthenticationFailed('Telegram init data expired')

        tg_user = data.get('user') or {}
        tg_id = str(tg_user.get('id') or '')
        if not tg_id:
            raise AuthenticationFailed('Telegram user id missing')

        user = TelegramAuthUser(
            tg_id=tg_id,
            username=tg_user.get('username') or '',
            first_name=tg_user.get('first_name') or '',
            last_name=tg_user.get('last_name') or '',
        )
        request.tg_init_data = data
        return user, None
