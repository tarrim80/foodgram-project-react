import re

from django.core.exceptions import ValidationError


def username_validator(username):
    """
    Проверка uername пользователя.
    """
    pattern = r"^[\w.@+-]+$"
    if not re.match(pattern, username):
        message = (
            "Username can only contain letters, "
            "numbers, and the following symbols: "
            ". @ + - _"
        )
        raise ValidationError(message)
