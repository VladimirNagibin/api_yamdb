from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly,
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
    permission_classes = (IsAdminOrReadOnly,)
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
    queryset = Title.objects.select_related('category').prefetch_related(
        'genre'
    ).annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('name', 'year')
    ordering = ('name',)
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
