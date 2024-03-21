from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models import NameModel, NameSlugModel


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
