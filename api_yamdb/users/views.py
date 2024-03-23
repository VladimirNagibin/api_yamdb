
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import CustomUser
from .permissions import AdminOrSuperUserOnly
from .serializers import (UserCreationSerializer, UserSerializer,
                          UserTokenCreationSerializer)
from .utils import confirm_send_mail


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет отвечающий за регистрацию пользователей
    и отправление кода подтверждения.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = UserCreationSerializer(data=request.data)
        if CustomUser.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ):
            user = CustomUser.objects.get(
                username=request.data.get('username'))
            serializer = UserCreationSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = request.data.get('username')
        user = CustomUser.objects.get(username=username)
        confirmation_code = default_token_generator.make_token(user)
        confirm_send_mail(user.email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTokenCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет отвечающий за получение токена."""
    queryset = CustomUser.objects.all()
    serializer_class = UserTokenCreationSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = UserTokenCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            user = get_object_or_404(CustomUser, username=username)
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')
            if not default_token_generator.check_token(
                user, confirmation_code
            ):
                return Response('Неверный код подтверждения',
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(str(AccessToken.for_user(user)),
                            status=status.HTTP_200_OK)


class AdminUserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Вьюсет отвечающий за работу с моделью CustomUser."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOrSuperUserOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        detail=False,
        methods=['GET', 'PATCH', 'DELETE'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user',
    )
    def get_user(self, request, username):
        """Функция отвечающая за работу с конкретным пользователем."""
        user = get_object_or_404(CustomUser, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        url_name='me',
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_patch_self(self, request):
        """Функция позволяющая получить данные о себе и редактировать их."""
        print(request.user.role)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save(role=request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
