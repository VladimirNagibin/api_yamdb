from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import NameModel, NameSlugModel

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


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
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
