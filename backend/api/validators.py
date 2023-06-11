import re

from django.core.exceptions import ValidationError


def validate_username(username):
    """
    Проверка uername пользователя.
    """
    pattern = r'^[\w.@+-]+$'
    if not re.match(pattern, username):
        message = ('Username can only contain letters, '
                   'numbers, and the following symbols: '
                   '. @ + - _')
        raise ValidationError(message)
