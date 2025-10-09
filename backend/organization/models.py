import uuid
from django.db import models

from core.utils import phone_validator


class District(models.Model):
    """Район (например, Урванский, Эльбрусский и т.д.)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True,
                            verbose_name="Название")

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Время изменения")

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Center(models.Model):
    """Молодежный центры в районе"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True,
                            verbose_name="Название")
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 related_name='center', verbose_name="Район")
    emblem = models.ImageField(upload_to='centers/emblems/', blank=True,
                               null=True, verbose_name="Иконка")
    address = models.CharField(max_length=255, blank=True, null=True,
                               verbose_name="Адрес")
    phone = models.CharField(max_length=15, validators=[phone_validator],
                             blank=True, null=True,
                             verbose_name="Номер телефона")

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Время изменения")

    class Meta:
        verbose_name = "Молодежный центр"
        verbose_name_plural = "Молодежные центры"
        ordering = ['name']

    def __str__(self):
        return self.name
