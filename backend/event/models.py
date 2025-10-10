import uuid

from django.db import models


class Event(models.Model):
    """Мероприятия которые мы будем парсить"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    period = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Время изменения")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['title']

    def __str__(self):
        return self.title
