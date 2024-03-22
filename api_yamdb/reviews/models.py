from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models import NameModel, NameSlugModel
from users.models import CustomUser


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
    genre = models.ManyToManyField(Genre, through='GenreTitle')


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Произведение')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments', verbose_name='Комментарий')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('id',)

    def __str__(self):
        return self.text
