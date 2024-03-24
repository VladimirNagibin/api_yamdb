import datetime as dt

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comments, Genre, Review, Title
from users.services import confirm_send_mail

User = get_user_model()


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
    author = SlugRelatedField(queryset=User.objects.all(),
                              slug_field='username',
                              default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        exclude = ('title',)

    def validate_author(self, author_value):
        """Проверка уникальности пары title-author через базу Review.

        Проверка выполняется через встроенную функцию validate сериализатора,
        а не get_object_or_404 для вывода требуемого по тестам кода ошибки -
        400, а не 404.
        """
        if Review.objects.filter(title=self.context['title_id'],
                                 author=author_value):
            raise serializers.ValidationError(
                'Невозможно создать второй отзыв на то же произведение!')
        return author_value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comments
        exclude = ('review',)


class ValidateUsernameMixin:
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Использование me запрещено')
        return value


class UserCreationSerializer(
    serializers.ModelSerializer,
    ValidateUsernameMixin
):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        confirm_send_mail(user.email, confirmation_code)
        return user


class UserTokenCreationSerializer(
    serializers.Serializer,
    ValidateUsernameMixin
):
    """Сериализатор для получения токена пользователем."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def create(self, validated_data):
        user = get_object_or_404(User, username=self.data.get('username'))
        if not default_token_generator.check_token(
            user, validated_data.get('confirmation_code')
        ):
            raise serializers.ValidationError('Неверный код потверждения')
        return str(AccessToken.for_user(user))


class UserSerializer(serializers.ModelSerializer, ValidateUsernameMixin):
    """Сериализатор для работы с моделью User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
