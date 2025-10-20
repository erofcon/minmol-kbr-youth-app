# booking/signals.py
import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Booking, Status
from core.telegram import notify_user, notify_owner

logger = logging.getLogger(__name__)


def _fmt_dt(dt):
    dt = timezone.localtime(dt) if timezone.is_aware(dt) else dt
    return dt.strftime("%d.%m.%Y %H:%M")


@receiver(pre_save, sender=Booking)
def booking_pre_save(sender, instance: Booking, **kwargs):
    # запоминаем прежний статус
    if not instance.pk:
        instance._old_status = None
        return
    try:
        old = Booking.objects.get(pk=instance.pk)
        instance._old_status = old.status
    except Booking.DoesNotExist:
        instance._old_status = None


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance: Booking, created: bool, **kwargs):
    room = instance.room
    room_title = room.title if room else "—"
    center_name = getattr(room.center, "name", None) if room and room.center_id else None
    address = (room.address or getattr(room.center, "address", None)) if room else None
    period = f"{_fmt_dt(instance.start_at)} — {_fmt_dt(instance.end_at)}"

    applicant_tg_id = instance.applicant_tg_id
    applicant_username = instance.applicant_tg_username

    if created:
        # Заявителю — подтверждение, что заявка на рассмотрении
        if applicant_tg_id:
            text_user = (
                f"📝 Заявка отправлена на рассмотрение\n\n"
                f"Помещение: <b>{room_title}</b>\n"
                f"Дата и время: <b>{period}</b>"
            )
            if center_name:
                text_user += f"\nЦентр: {center_name}"
            if address:
                text_user += f"\nАдрес: {address}"
            text_user += "\n\nМы уведомим вас о решении."
            notify_user(applicant_tg_id, text_user)

        # Ответственному — новая заявка
        owner_tg_id = room.responsible.telegram_id if (room and room.responsible and room.responsible.telegram_id) else None
        if owner_tg_id:
            text_owner = (
                f"📩 Новая заявка на бронирование\n\n"
                f"Помещение: <b>{room_title}</b>\n"
                f"Дата и время: <b>{period}</b>"
            )
            if center_name:
                text_owner += f"\nЦентр: {center_name}"
            if address:
                text_owner += f"\nАдрес: {address}"
            text_owner += f"\n\nЗаявитель: <b>{instance.applicant_name}</b>"
            if applicant_username:
                text_owner += f" (@{applicant_username})"
            if instance.applicant_phone:
                text_owner += f"\nТелефон: {instance.applicant_phone}"
            text_owner += f"\n\nМероприятие: <b>{instance.event_name}</b>"
            notify_owner(owner_tg_id, text_owner)

        return

    # Изменение существующей — проверяем смену статуса
    old_status = getattr(instance, "_old_status", None)
    if old_status == instance.status:
        return

    if instance.status == Status.APPROVED and applicant_tg_id:
        text = (
            f"✅ Ваша заявка одобрена!\n\n"
            f"Помещение: <b>{room_title}</b>\n"
            f"Дата и время: <b>{period}</b>"
        )
        if center_name:
            text += f"\nЦентр: {center_name}"
        if address:
            text += f"\nАдрес: {address}"
        notify_user(applicant_tg_id, text)

    elif instance.status == Status.REJECTED and applicant_tg_id:
        reason = (instance.rejection_reason or "").strip() or "Причина не указана"
        text = (
            f"❌ Ваша заявка отклонена.\n\n"
            f"Помещение: <b>{room_title}</b>\n"
            f"Дата и время: <b>{period}</b>\n"
            f"Причина: {reason}"
        )
        notify_user(applicant_tg_id, text)

    elif instance.status == Status.CANCELED and applicant_tg_id:
        text = (
            f"⚠️ Ваша заявка отменена.\n\n"
            f"Помещение: <b>{room_title}</b>\n"
            f"Дата и время: <b>{period}</b>"
        )
        notify_user(applicant_tg_id, text)