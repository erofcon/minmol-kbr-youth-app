import time
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import CustomUser
from .telegram import verify_init_data


class TelegramInitDataAuthentication(BaseAuthentication):
    """
    Ищет initData в:
    - заголовке X-Telegram-Init-Data
    - query-параметре init_data
    - теле запроса (form/json) под ключом init_data
    Валидирует подпись, проверяет TTL, маппит/создаёт локального пользователя по telegram_id.
    """
    header_name = 'HTTP_X_TELEGRAM_INIT_DATA'

    def authenticate(self, request):
        init_data = (
                request.META.get(self.header_name)
                or request.query_params.get('init_data')
                or (request.data.get('init_data') if hasattr(request,
                                                             'data') else None)
        )

        if not init_data:
            # Нет данных — дальше пусть DRF решает (но у нас других аутентификаторов нет)
            return None

        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if not bot_token:
            raise AuthenticationFailed('Telegram bot token not configured')

        try:
            data = verify_init_data(init_data, bot_token)
        except Exception:
            raise AuthenticationFailed('Invalid Telegram init data')

        # TTL
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

        # upsert локального пользователя по telegram_id
        user, created = CustomUser.objects.get_or_create(
            telegram_id=tg_id,
            defaults={
                'username': f'tg_{tg_id}',
                'first_name': tg_user.get('first_name', '') or '',
                'last_name': tg_user.get('last_name', '') or '',
            }
        )
        # легкое обновление имён (без изменения username)
        updated = False
        fn = tg_user.get('first_name') or ''
        ln = tg_user.get('last_name') or ''
        if user.first_name != fn:
            user.first_name = fn
            updated = True
        if user.last_name != ln:
            user.last_name = ln
            updated = True
        if updated:
            user.save(update_fields=['first_name', 'last_name'])

        # сохраним initData на реквесте — пригодится в вьюхах
        request.tg_init_data = data

        return user, None
