import uuid

from django.db import models

from user.models import CustomUser


class Status(models.TextChoices):
    PENDING = "PENDING", "В ожидании"
    APPROVED = "APPROVED", "Одобрено"
    REJECTED = "REJECTED", "Отклонено"
    CANCELED = "CANCELED", "Отменено"


class RoomTag(models.Model):
    """Теги помещении, например wi-fi, playstation 4 и т.д."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Тег помещения"
        verbose_name_plural = "Теги помещений"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    """Помещение для бронирования"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    capacity = models.PositiveIntegerField(default=0, verbose_name="Вмещаемость")
    image = models.ImageField(upload_to="rooms/images/", blank=True, null=True, verbose_name="Изображение",
                              help_text="Возможно добавить только одно изображение")
    tags = models.ManyToManyField(RoomTag, blank=True, related_name="rooms", verbose_name="Теги помещении")
    responsible = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="responsible_for_rooms", verbose_name="Ответсвенный за помещение",
        help_text="ФИО и номер телефона данного сотрудника увидят внешние пользователи Telegram(если заполнен). "
                  "Если у сотрудника заполнен Telegram ID, то он получит уведомление при поступлении заявки бронирования.")

    class Meta:
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"

    def __str__(self):
        return self.title


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, related_name="bookings", )

    # Информация от пользователья

    applicant_name = models.CharField(max_length=255, blank=False, null=False)
    applicant_tg_username = models.CharField(max_length=255, blank=False, null=False)



























