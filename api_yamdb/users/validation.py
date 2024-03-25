import re

from django.core.exceptions import ValidationError


def validate_username(value, **args):
    if value == 'me':
        raise ValidationError('Использование me запрещено')
    string = re.match(r'^[\w.@+-]+$', value)
    if not string:
        raise ValidationError('Некорректное имя')
    return value
