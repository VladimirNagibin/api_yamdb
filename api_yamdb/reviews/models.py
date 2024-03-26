from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import NameModel, NameSlugModel, TextAuthorPubDateModel
from .constants import MAX_SCORE, MIN_SCORE, MIN_YEAR_TITLES
from .validations import get_current_year

User = get_user_model()


class Category(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(NameModel):
    year = models.SmallIntegerField(
        validators=(
            MaxValueValidator(get_current_year,
                              message='Проверьте год выпуска!'),
            MinValueValidator(MIN_YEAR_TITLES,
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


class Review(TextAuthorPubDateModel):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)),
        verbose_name='Оценка'
    )

    class Meta(TextAuthorPubDateModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comments(TextAuthorPubDateModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta(TextAuthorPubDateModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
