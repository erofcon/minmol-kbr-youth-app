from urllib.parse import parse_qsl
import hashlib
import hmac
import json


def _compute_webapp_secret_key(bot_token: str) -> bytes:
    # secret_key = HMAC_SHA256("WebAppData", bot_token)
    return hmac.new(b'WebAppData', bot_token.encode('utf-8'),
                    hashlib.sha256).digest()


def _build_data_check_string(data: dict) -> str:
    return '\n'.join(f'{k}={v}' for k, v in sorted(data.items()))


def verify_init_data(init_data: str, bot_token: str) -> dict:
    """
    Валидирует initData из Telegram WebApp.
    Возвращает dict с полями initData, где user уже распарсен в dict.
    Бросает ValueError при невалидной подписи.
    """
    if not init_data:
        raise ValueError('init_data is empty')

    data = dict(parse_qsl(init_data, strict_parsing=True))
    received_hash = data.pop('hash', None)
    if not received_hash:
        raise ValueError('hash is missing')

    check_string = _build_data_check_string(data)
    secret_key = _compute_webapp_secret_key(bot_token)
    calculated_hash = hmac.new(secret_key, check_string.encode('utf-8'),
                               hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError('invalid hash')

    # Преобразуем user из JSON-строки (если есть)
    user_raw = data.get('user')
    if user_raw:
        try:
            data['user'] = json.loads(user_raw)
        except Exception:
            # если почему-то некорректный JSON — тоже запретим
            raise ValueError('invalid user json')

    return data
