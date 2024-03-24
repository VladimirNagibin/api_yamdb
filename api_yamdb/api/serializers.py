from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.constants import NAME_MAX_LENGHT
from reviews.models import Title, Genre, Category, Review, Comments
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoryRelatedField(SlugRelatedField):
    def to_representation(self, value):
        return CategorySerializer(value).data


class GenreRelatedField(SlugRelatedField):
    def to_representation(self, value):
        return GenreSerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True, default=0)
    description = serializers.CharField(required=False)
    category = CategoryRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = GenreRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        allow_null=False,
        allow_empty=False
    )
    name = serializers.CharField(max_length=NAME_MAX_LENGHT)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(queryset=CustomUser.objects.all(),
                              slug_field='username',
                              default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        exclude = ('title',)

    def validate_author(self, author_value):
        """Проверка уникальности пары title-author через базу Review."""
        title_value = get_object_or_404(Title, pk=self.context['title_id'])
        if Review.objects.filter(title=title_value, author=author_value):
            raise serializers.ValidationError(
                'Невозможно создать второй отзыв на то же произведение!')
        return author_value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comments
        exclude = ('review',)
