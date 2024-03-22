import datetime as dt

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

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
    rating = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    category = CategoryRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = GenreRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    name = serializers.CharField(max_length=256)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        if not (0 < value <= dt.date.today().year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError('Не передали слаги жанров!')
        return value

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return round(rating, 2)


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
        if Review.objects.filter(
            title=title_value, author=author_value
        ).exists() and self.context['request'].method != 'PUT':
            raise serializers.ValidationError(
                'Невозможно создать второй отзыв на то же произведение!')
        return author_value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comments
        exclude = ('review',)
