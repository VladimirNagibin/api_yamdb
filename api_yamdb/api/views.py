from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrSuperuserOrReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, ReviewSerializer
)
from reviews.models import Category, Genre, Title


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для операций с моделью Review."""

    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_title_object(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_serializer_context(self):
        return {'title_id': self.kwargs['title_id']}

    def perform_create(self, serializer):
        """Переопределение единичной операции сохранения объекта модели."""
        serializer.save(
            # author=self.request.user,  # подключаем по мере готовности User
            title=self.get_title_object()
        )

    def get_queryset(self):
        return self.get_title_object().reviews.all()
