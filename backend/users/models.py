from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя (дополненная)."""
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        help_text='Обязательное поле. Имя пользователя.'
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        help_text='Обязательное поле. Фамилия пользователя.'
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        db_index=True,
        help_text='Обязательное поле. Введите существующий '
        'адрес электронной почты.'
    )
    is_staff = models.BooleanField(
        'администратор',
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    def __str__(self):
        return self.get_full_name()
