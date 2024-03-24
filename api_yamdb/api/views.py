from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (AdminOrSuperUserOnly, IsAdminOrAuthorOrReadOnly,
                          IsAdminOrSuperuserOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserCreationSerializer, UserSerializer,
                          UserTokenCreationSerializer)
from users.models import User
from users.services import confirm_send_mail


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (IsAdminOrSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrSuperuserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для операций с моделью Review."""

    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']  # 'PUT' excluding
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    def get_title_object(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_serializer_context(self):
        """Добавление дополнительных данных для передачи в сериализатор."""
        return {'title_id': self.kwargs['title_id'],
                'request': self.request}

    def perform_create(self, serializer):
        """Переопределение единичной операции сохранения объекта модели."""
        serializer.save(
            author=self.request.user,
            title=self.get_title_object()
        )

    def get_queryset(self):
        return self.get_title_object().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для операций с моделью Comment."""

    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']  # 'PUT' excluding
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    def get_review_object(self):
        title_value = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                 title=title_value)

    def perform_create(self, serializer):
        """Переопределение единичной операции сохранения объекта модели."""
        serializer.save(
            author=self.request.user,
            review=self.get_review_object()
        )

    def get_queryset(self):
        return self.get_review_object().comments.all()

    def get_serializer_context(self):
        """Добавление дополнительных данных для передачи в сериализатор."""
        return {'title_id': self.kwargs['title_id'],
                'review_id': self.kwargs['review_id']}


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup(request):
    """Вью отвечающая за регистрацию пользователей."""
    serializer = UserCreationSerializer(data=request.data)
    user = User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')).first()
    if user:
        confirmation_code = default_token_generator.make_token(user)
        confirm_send_mail(user.email, confirmation_code)
        return Response(
            'Код выслан повторно на почту',
            status=status.HTTP_200_OK
        )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def get_token(request):
    """Вью отвечающая за получение токена."""
    serializer = UserTokenCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = serializer.save()
    return Response(f'{token}', status=status.HTTP_200_OK)


class AdminUserViewSet(viewsets.ModelViewSet):
    """Вьюсет отвечающий за работу с моделью CustomUser."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AdminOrSuperUserOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET'],
        url_name='me',
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_self(self, request):
        """Функция позволяющая получить данные о себе."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_self.mapping.patch
    def patch_me(self, request):
        """Функция позволяющая редактировать данные о себе."""
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
