from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

from core.utils import phone_validator


class CustomUser(AbstractUser):
    """Кастомный пользователь"""

    telegram_id = models.CharField(max_length=50, unique=True, blank=True,
                                   null=True, verbose_name="Telegram ID",
                                   help_text="ID пользователя в Телеграмме. "
                                             "Заполняется если пользователь должен получать уведомление через Телеграмм "
                                             "(после того как его сделают ответственным за помещение).")

    phone = models.CharField(max_length=15, validators=[phone_validator],
                             blank=True, null=True,
                             verbose_name='Номер телефона',
                             help_text="Этот номер увидят те, кто бронируют помещения")

    def __str__(self):
        full_name = self.get_full_name()

        if full_name.strip():
            return full_name

        return self.username


class GroupProxy(Group):
    class Meta:
        proxy = True
        app_label = 'user'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
