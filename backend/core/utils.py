from django.core.validators import RegexValidator

phone_validator = RegexValidator(regex=r'^\+?\d{10,15}$',
                                 message="Введите телефон в формате +79991234567")
