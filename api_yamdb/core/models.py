from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import NAME_MAX_LENGHT, SLUG_MAX_LENGHT, TEXT_LIMIT

User = get_user_model()


class NameModel(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGHT)

    def __str__(self):
        return self.name[:TEXT_LIMIT]

    class Meta:
        abstract = True
        ordering = ('name',)


class NameSlugModel(NameModel):
    slug = models.SlugField('Слаг', unique=True, max_length=SLUG_MAX_LENGHT)

    class Meta(NameModel.Meta):
        abstract = True


class TextAuthorPubDateModel(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:TEXT_LIMIT]
