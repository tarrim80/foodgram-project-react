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
        'адрес электронной почты.',
        error_messages={'unique': ('Пользователь с таким адресом электронной '
                        'почты уже существует')}
    )
    is_staff = models.BooleanField(
        'администратор',
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    def __str__(self):
        if self.first_name or self.last_name:
            return self.get_full_name()
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Пользователь, который оформил подписку',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор контента',
        help_text='Пользователь, на которого оформлена подписка',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follower'
            ),
        )

    def __str__(self) -> str:
        return (f'{self.user} подписан на рецепты, которые разместил(а)'
                f' {self.author}')
