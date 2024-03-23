
from rest_framework import serializers

from .models import CustomUser


class UserCreationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использование me запрещено')
        return data


class UserTokenCreationSerializer(serializers.Serializer):
    """Сериализатор для получения токена пользователем."""
    username = serializers.CharField(max_length=50, required=True)
    confirmation_code = serializers.CharField(max_length=254, required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью User."""

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
