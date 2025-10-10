import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

from core.utils import phone_validator
from user.models import CustomUser
from organization.models import Center


class Status(models.TextChoices):
    PENDING = "PENDING", "В ожидании"
    APPROVED = "APPROVED", "Одобрено"
    REJECTED = "REJECTED", "Отклонено"
    CANCELED = "CANCELED", "Отменено"


class RoomTag(models.Model):
    """Теги помещении, например wi-fi, playstation 4 и т.д."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True,
                            verbose_name="Название")

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Время изменения")

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
    capacity = models.PositiveIntegerField(default=0,
                                           verbose_name="Вмещаемость")
    image = models.ImageField(upload_to="rooms/images/", blank=True, null=True,
                              verbose_name="Изображение",
                              help_text="Возможно добавить только одно изображение")
    tags = models.ManyToManyField(RoomTag, blank=True, related_name="rooms",
                                  verbose_name="Теги помещении")

    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True,
                               blank=True, related_name="center_for_rooms",
                               verbose_name="Молодежный центр",
                               help_text="Какому Молодежному центру принадлежит это помещение")

    is_active = models.BooleanField(default=True, verbose_name="Активное помещение",
                                    help_text="Указывает, следует ли считать это помещение активным. "
                                              "Можно снять это выделение вместо удаления, "
                                              "тогда пользователи не увидят помещение в Telegram")

    responsible = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="responsible_for_rooms",
        verbose_name="Ответсвенный за помещение",
        help_text="Если у сотрудника заполнен Telegram ID, то он получит уведомление при поступлении заявки "
                  "бронирования.")

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Время изменения")

    class Meta:
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"

    def __str__(self):
        return self.title


USER_INFO_FIELDS = (
    "room", "start_at", "end_at",
    "applicant_name", "applicant_tg_username", "applicant_phone",
    "event_name", "event_purpose", "target_audience",
    "invited_speakers", "required_equipment",
)


class Booking(models.Model):
    """Заявки на бронирования"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=False,
                             null=True, related_name="bookings",
                             verbose_name="Помещение")

    status = models.CharField(max_length=10, choices=Status.choices,
                              default=Status.PENDING,
                              verbose_name="Текущий статус бронирования",
                              help_text="Для одобрения или отклонения запроса на бронирование необходимо отредактировать этот пункт")

    rejection_reason = models.TextField(blank=True,
                                        verbose_name="Причина отклонения",
                                        help_text="При отклонении обязательно необходимо заполнить причину отклонения")

    # Информация от пользователья
    start_at = models.DateTimeField(verbose_name="Начало бронирования",
                                    help_text="Дата и время начала бронирования")

    end_at = models.DateTimeField(verbose_name="Окончание бронирования",
                                  help_text="Дата и время окончания бронирования")

    applicant_name = models.CharField(max_length=255,
                                      verbose_name="Имя заявителя")

    applicant_tg_username = models.CharField(max_length=255, blank=False,
                                             null=False,
                                             verbose_name="Имя заявителя в Telegram")

    applicant_phone = models.CharField(max_length=15,
                                       validators=[phone_validator],
                                       verbose_name="Номер телефона заявителя")

    event_name = models.CharField(max_length=255,
                                  verbose_name="Название мероприятия")

    event_purpose = models.CharField(max_length=255,
                                     verbose_name="Цель мероприятия")

    target_audience = models.CharField(max_length=255,
                                       verbose_name="Целевая аудитория")

    invited_speakers = models.CharField(max_length=255,
                                        verbose_name="Приглашенные спикеры")

    required_equipment = models.CharField(max_length=255,
                                          verbose_name="Список необходимого оборудования")

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Время изменения")

    def __str__(self):
        room_name = self.room.title if self.room else "Без помещения"
        status = self.get_status_display()
        start = self.start_at.strftime("%d.%m.%Y %H:%M")
        return f"Бронь {room_name} ({status}) с {start}"

    def clean(self):
        if self.status == Status.REJECTED and not (
                self.rejection_reason or "").strip():
            raise ValidationError(
                {"rejection_reason": "Укажите причину отклонения.😣"})

        if self.status == Status.APPROVED and (
                self.rejection_reason).strip():
            raise ValidationError(
                {
                    "rejection_reason": "При одобрении указывать причину отклонения не нужно.😃"})

        if self.end_at <= self.start_at:
            raise ValidationError(
                {"end_at": "Окончание бронирования должно быть позже начала."})

    @classmethod
    def allowed_statuses_for(cls, user):
        if user.is_superuser:
            return [c for c, _ in Status.choices]
        return [Status.APPROVED, Status.REJECTED]

    def validate_status_for_user(self, user):
        if self.status not in self.allowed_statuses_for(user):
            raise ValidationError(
                {"status": "Недопустимый статус для вашей роли."})

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="booking_rejection_reason_required_on_rejected",
                check=~Q(status=Status.REJECTED) | ~Q(rejection_reason=""),
            )
        ]

        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]
