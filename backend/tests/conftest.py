import os
import sys

import django
from django.utils.version import get_version
from foodgram_backend.settings.base import INSTALLED_APPS

django.setup()

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = 'backend'

if (
        PROJECT_DIR_NAME not in root_dir_content
        or not os.path.isdir(os.path.join(BASE_DIR, PROJECT_DIR_NAME))
):
    assert False, (
        f'В директории `{BASE_DIR}` не найдена папка c проектом '
        f'`{PROJECT_DIR_NAME}`. Убедитесь, что у вас верная структура проекта.'
    )

MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = 'manage.py'

if FILENAME not in project_dir_content:
    assert False, (
        f'В директории `{MANAGE_PATH}` не найден файл `{FILENAME}`. '
        f'Убедитесь, что у вас верная структура проекта.'
    )

assert get_version() < '4.0.0', 'Пожалуйста, используйте версию Django < 4.0.0'

APPS_LIST = [
    ['users.apps.UsersConfig', 'users'],
    ['api.apps.APIConfig', 'api'],
    ['recipes.apps.RecipesConfig', 'recipes']
]

for row in APPS_LIST:
    assert any(app in INSTALLED_APPS for app in row), (
        f'Пожалуйста зарегистрируйте приложение `{row[1]}`'
        f' в `settings.INSTALLED_APPS`'
    )

pytest_plugins = [
    'tests.fixtures.fixture_user',
]
