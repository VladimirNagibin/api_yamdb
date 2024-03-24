from django.db import models

from reviews.constants import NAME_MAX_LENGHT, SLUG_MAX_LENGHT


class NameModel(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGHT)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('name',)


class NameSlugModel(NameModel):
    slug = models.SlugField('Слаг', unique=True, max_length=SLUG_MAX_LENGHT)

    class Meta(NameModel.Meta):
        abstract = True
