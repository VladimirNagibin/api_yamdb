from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    USER = 'User'
    ADMIN = 'Admin'
    MODERATOR = 'Moderator'
    ROLE_CHOICES = (
        (USER, 'User'),
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Некорректное имя пользователя')]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль')
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
