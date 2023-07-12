import os
import sys

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.core.management import call_command
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from users.models import User


@receiver(post_save, sender=User)
def assign_admin_group(sender, instance, **kwargs):
    """
    Добавление пользователя в группу Администраторов или удаление из неё
    в зависимости от состояния свойства `is_staff`
    """
    admin_group, _ = Group.objects.get_or_create(name='Администраторы')
    if instance.is_staff:
        instance.groups.add(admin_group)
    else:
        instance.groups.remove(admin_group)


@receiver(post_migrate)
def load_data_after_migration(sender, **kwargs):
    """
    Загрузка фиктивных данных спарсенных с сайта `food.ru` для тестирования
    работы ресурса. Загрузка срабатывает только один раз после первой
    миграции моделей приложений `users` и `recipes` и только в процессе
    разработки.
    """
    if os.getenv('DEVELOPMENT_STATUS') == 'PRODUCTION':
        return

    # if sender.name not in ('users', 'recipes'):
    if sender.name != 'users':
        return

    migration_recorders = MigrationRecorder(connection).migration_qs
    users_migration_count = migration_recorders.filter(app='users').count()
    recipes_migration_count = migration_recorders.filter(
        app='recipes').count()
    migration_counts = (users_migration_count, recipes_migration_count)
    if not all(mc == 1 for mc in migration_counts):
        sys.stdout.write(
            'Фиктивные данные могут быть загружены '
            'только после первой миграции пользовательских моделей! \n'
        )
        return

    data_dir = settings.BASE_DIR / 'data'
    fixture_files = list(os.path.join(data_dir, file)
                         for file in os.listdir(data_dir))
    call_command(
        'loaddata', *fixture_files)
