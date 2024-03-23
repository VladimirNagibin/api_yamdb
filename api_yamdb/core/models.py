from django.db import models


class NameModel(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('name',)


class NameSlugModel(NameModel):
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta(NameModel.Meta):
        abstract = True
