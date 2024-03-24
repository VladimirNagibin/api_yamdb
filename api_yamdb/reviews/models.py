import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import NameModel, NameSlugModel

User = get_user_model()

TEXT_LIMIT = 50


class Category(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(NameModel):
    year = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(dt.date.today().year,
                              message='Проверьте год выпуска!'),
        ),
        verbose_name='Год выпуска',
        db_index=True
    )
    description = models.TextField('Описание')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория',
                                 null=True,
                                 blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')

    class Meta(NameModel.Meta):
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:TEXT_LIMIT]


class Comments(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Комментарий'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:TEXT_LIMIT]
