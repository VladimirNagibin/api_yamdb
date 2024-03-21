import datetime as dt

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from reviews.models import Title, Genre, Category, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(read_only=True, slug_field='username')
    author = serializers.IntegerField(read_only=True, default=1)  # заменить
    # title = serializers.HiddenField()

    class Meta:
        exclude = ('title',)
        # fields = '__all__'
        model = Review

        validators = [
            UniqueTogetherValidator(queryset=Review.objects.all(),
                                    fields=('text', 'author'))
        ]

    def create(self, validated_data):
        title_id = self.context['title_id']
        print('title_id = ', title_id)
        validated_data['title'] = get_object_or_404(Title, pk=title_id)
        return super(ReviewSerializer, self).create(validated_data)

    # def get_title_object(self):
    #     title_id = self.context['title_id']
    #     return get_object_or_404(Title, pk=title_id)
