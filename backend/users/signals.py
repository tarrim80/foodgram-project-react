import os
import sys
from datetime import datetime as dt

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from users.models import User


@receiver(post_save, sender=User)
def assign_admin_group(sender, instance, **kwargs):
    """
    Добавление пользователя в группу Администраторов или удаление из неё
    в зависимости от состояния свойства `is_staff`.
    """
    admin_group, _ = Group.objects.get_or_create(name="Администраторы")
    if instance.is_staff:
        instance.groups.add(admin_group)
    else:
        instance.groups.remove(admin_group)


@receiver(post_migrate)
def after_migration(sender, **kwargs):
    """Сигнал срабатывающий после выполнения миграций БД."""
    load_mock_data(sender, **kwargs)
    set_admin_permissions(sender, **kwargs)


def load_mock_data(sender, **kwargs):
    """
    Загрузка фиктивных данных спарсенных с сайта `food.ru` для тестирования
    работы ресурса.

    Загрузка срабатывает только один раз после первой
    миграции моделей приложений `users` и `recipes` и только в процессе
    разработки.
    """
    if os.getenv("DEVELOPMENT_STATUS") == "PRODUCTION":
        return

    if sender.name != "users":
        return

    migration_recorder = MigrationRecorder(connection)
    applied_migrations = migration_recorder.applied_migrations()

    appropriate_entries = []
    for migration in applied_migrations.values():
        if migration.app in ("users", "recipes"):
            appropriate_entries.append(migration)

    migration_names, migration_times = [], []
    for entry in appropriate_entries:
        migration_names.append(entry.name.split("_")[-1])
        migration_times.append(entry.applied.replace(tzinfo=None))

    time_last_migration = max(time for time in migration_times)
    time_since_last_migration = (
        dt.utcnow() - time_last_migration
    ).total_seconds()
    time_is_appropriate = (
        time_since_last_migration < settings.MIGRATION_LIFETIME_SEC
    )

    if not time_is_appropriate:
        return

    if not all(name == "initial" for name in migration_names):
        sys.stdout.write(
            "Фиктивные данные могут быть загружены "
            "только после первой миграции пользовательских моделей! \n"
        )
        return

    data_dir = settings.BASE_DIR / "mock_data"
    fixture_files = list(
        os.path.join(data_dir, file) for file in os.listdir(data_dir)
    )
    call_command("loaddata", *fixture_files)


def set_admin_permissions(sender, **kwargs):
    """Установка прав администраторов после обновления БД."""

    admin_group, _ = Group.objects.get_or_create(name="Администраторы")
    admin_group.save()

    permissions = Permission.objects.all()
    admin_group.permissions.set(permissions)
