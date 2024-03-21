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
