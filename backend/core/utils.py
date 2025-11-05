from django.core.validators import RegexValidator
from rest_framework import serializers

phone_validator = RegexValidator(regex=r'^\+?\d{10,15}$',
                                 message="Введите телефон в формате +79991234567")


class AbsoluteHTTPSImageField(serializers.ImageField):
    def to_representation(self, value):
        url = super().to_representation(value)
        if not url:
            return None
        if url.startswith('http://'):
            return 'https://' + url[len('http://'):]

        return url
