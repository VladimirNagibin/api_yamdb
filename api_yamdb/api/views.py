
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .filters import TitleFilter
from .permissions import (IsAdminOrSuperuserOrReadOnly,
                          IsAdminOrAuthorOrReadOnly)
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)
from reviews.models import Category, Genre, Title, Review


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
    pagination_class = PageNumberPagination

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
    pagination_class = PageNumberPagination

    def get_review_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        """Переопределение единичной операции сохранения объекта модели."""
        serializer.save(
            author=self.request.user,
            review=self.get_review_object()
        )

    def get_queryset(self):
        return self.get_review_object().comments.all()
