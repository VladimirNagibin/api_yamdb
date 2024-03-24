from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .constants import (ADMIN, EMAIL_FIELD_LENGTH, MAX_ROLE_LENGTH, MODERATOR,
                        ROLE_CHOICES, STANDARD_FIELD_LENGTH, USER)


class User(AbstractUser):
    username = models.CharField(
        max_length=STANDARD_FIELD_LENGTH,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Некорректное имя пользователя')]
    )
    email = models.EmailField(
        max_length=EMAIL_FIELD_LENGTH,
        unique=True,
        verbose_name='Почта'
    )
    first_name = models.CharField(
        max_length=STANDARD_FIELD_LENGTH,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=STANDARD_FIELD_LENGTH,
        blank=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
