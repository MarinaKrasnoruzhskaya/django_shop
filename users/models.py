from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from blog.models import NULLABLE


class User(AbstractUser):
    """Класс для пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите email')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', help_text='Введите номер телефона', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', help_text='Введите страну', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
