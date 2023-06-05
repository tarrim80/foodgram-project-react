from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_staff = models.BooleanField(
        'администратор',
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
