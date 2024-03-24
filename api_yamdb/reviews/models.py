from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import MIN_SCORE, MAX_SCORE
from core.models import NameModel, NameSlugModel, TextAuthorPubDateModel

User = get_user_model()

TEXT_LIMIT = 50


class Category(NameSlugModel):
    pass


class Genre(NameSlugModel):
    pass


class Title(NameModel):
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True)
    genre = models.ManyToManyField(Genre)


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
