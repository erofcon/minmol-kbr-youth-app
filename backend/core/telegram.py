from urllib.parse import parse_qsl
import hashlib
import hmac
import json
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


def _compute_webapp_secret_key(bot_token: str) -> bytes:
    return hmac.new(b'WebAppData', bot_token.encode('utf-8'), hashlib.sha256).digest()


def _build_data_check_string(data: dict) -> str:
    return '\n'.join(f'{k}={v}' for k, v in sorted(data.items()))


def verify_init_data(init_data: str, bot_token: str) -> dict:
    if not init_data:
        raise ValueError('init_data is empty')

    data = dict(parse_qsl(init_data, strict_parsing=True))
    received_hash = data.pop('hash', None)
    if not received_hash:
        raise ValueError('hash is missing')

    check_string = _build_data_check_string(data)
    secret_key = _compute_webapp_secret_key(bot_token)
    calculated_hash = hmac.new(secret_key, check_string.encode('utf-8'), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError('invalid hash')

    user_raw = data.get('user')
    if user_raw:
        try:
            data['user'] = json.loads(user_raw)
        except Exception:
            raise ValueError('invalid user json')

    return data


def send_telegram_message(bot_token: str, chat_id: str | int, text: str,
                          parse_mode: Optional[str] = "HTML", protect_content: bool = False) -> bool:
    """
    Безопасная отправка сообщений Телеграм. Возвращает True/False.
    """
    if not bot_token:
        logger.warning("Telegram token is empty, skip sending.")
        return False
    if not chat_id or not text:
        logger.warning("Missing chat_id or text, skip sending.")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
        "protect_content": protect_content,
    }

    try:
        resp = requests.post(url, json=payload, timeout=7)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            logger.error("Telegram API error: %s", data)
            return False
        return True
    except Exception as e:
        logger.exception("Telegram sendMessage failed: %s", e)
        return False


def notify_user(chat_id: str | int, text: str, parse_mode: Optional[str] = "HTML") -> bool:
    from django.conf import settings
    return send_telegram_message(getattr(settings, "TELEGRAM_BOT_TOKEN", ""), chat_id, text, parse_mode)


def notify_owner(chat_id: str | int, text: str, parse_mode: Optional[str] = "HTML") -> bool:
    """
    Уведомления ответственным через отдельный бот. Если не задан, упадём на user-бот.
    """
    from django.conf import settings
    token = getattr(settings, "TELEGRAM_OWNER_BOT_TOKEN", "") or getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    return send_telegram_message(token, chat_id, text, parse_mode)