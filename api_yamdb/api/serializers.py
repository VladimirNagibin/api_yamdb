import datetime as dt

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Title, Genre, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoryField(serializers.Field):
    def to_representation(self, value):
        return CategorySerializer(value).data

    def to_internal_value(self, data):
        return get_object_or_404(Category, slug=data)


class GenreField(serializers.Field):
    def to_representation(self, value):
        return GenreSerializer(value, many=True).data

    def to_internal_value(self, data):
        return [get_object_or_404(Genre, slug=slug) for slug in data]


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    category = CategoryField()
    genre = GenreField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        if not (0 < value <= dt.date.today().year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def get_rating(self, obj):
        # rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        # if rating:
        #    return round(rating, 2)
        return 5
