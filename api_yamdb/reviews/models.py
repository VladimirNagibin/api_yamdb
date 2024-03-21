from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,  # модель Title подключаем из другой ветки проекта
        on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Произведение')
    text = models.TextField(verbose_name='Текст')
    author = models.IntegerField(default=1)
    # author = models.ForeignKey(
    #     #  модель User подключаем из другой ветки проекта
    #     User,
    #     on_delete=models.CASCADE, related_name='reviews',
    #     verbose_name='Автор'
    # )
    score = models.IntegerField(
        default=10,
        validators=[
            MinValueValidator(1), MaxValueValidator(10)
        ],
        verbose_name='Рейтинг')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    ...
