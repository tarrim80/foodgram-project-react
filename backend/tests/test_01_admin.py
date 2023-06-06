import re

import pytest
from django.contrib.admin.sites import site
from django.db.models import fields
# from django.template.loader import get_template, select_template


try:
    from users.models import User
except ImportError:
    assert False, 'Не найдена модель User'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def search_refind(execution, user_code):
    """Поиск запуска"""
    for temp_line in user_code.split('\n'):
        if re.search(execution, temp_line):
            return True
    return False


class TestAdminUser:

    @pytest.mark.django_db(transaction=True)
    def test_user_admin(self):
        first_name = 'Имя'
        last_name = 'Фамилия'
        username = 'test_username'
        email = 'test@foodgram.fake'

        assert User.objects.all().count() == 0

        user = User.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   username=username,
                                   email=email)
        assert User.objects.all().count() == 1
        assert User.objects.get(username=username, email=email).pk == user.pk

        admin_site = site

        assert User in admin_site._registry, (
            'Зарегистрируйте модель `User` в админской панели'
        )

        admin_model = admin_site._registry[User]

        assert 'username' in admin_model.list_display, (
            'Добавьте `username` для отображения в списке '
            'модели административного сайта'
        )
        assert 'email' in admin_model.list_display, (
            'Добавьте `email` для отображения в списке '
            'модели административного сайта'
        )
        assert 'first_name' in admin_model.list_display, (
            'Добавьте `first_name` для отображения в списке '
            'модели административного сайта'
        )
        assert 'last_name' in admin_model.list_display, (
            'Добавьте `last_name` для отображения в списке '
            'модели административного сайта'
        )
        assert 'is_staff' in admin_model.list_display, (
            'Добавьте `is_staff` для отображения в списке '
            'модели административного сайта'
        )

        assert 'username' in admin_model.list_filter, (
            'Добавьте `username` для фильтрации модели административного сайта'
        )
        assert 'email' in admin_model.list_filter, (
            'Добавьте `email` для фильтрации модели административного сайта'
        )

        assert 'username' in admin_model.search_fields, (
            'Добавьте `username` для поиска в модели административного сайта'
        )
        assert 'email' in admin_model.search_fields, (
            'Добавьте `email` для поиска в модели административного сайта'
        )

        assert 'username' in admin_model.prepopulated_fields, (
            'Добавьте `username` для предзаполнения из Имени и Фамилии'
        )
        assert ('first_name', 'last_name') in (
            admin_model.prepopulated_fields.values()), (
            'Добавьте `first_name` и `last_name`'
            ' для предзаполнения в `username`'
        )

        assert hasattr(admin_model, 'empty_value_display'), (
            'Добавьте дефолтное значение `-пусто-` для пустого поля'
        )
        assert admin_model.empty_value_display == '-пусто-', (
            'Добавьте дефолтное значение `-пусто-` для пустого поля'
        )


# class TestGroup:

#     def test_group_model(self):
#         model_fields = Group._meta.fields
#         title_field = search_field(model_fields, 'title')
#         assert title_field is not None, 'Добавьте название события `title` модели `Group`'
#         assert type(title_field) == fields.CharField, (
#             'Свойство `title` модели `Group` должно быть символьным `CharField`'
#         )
#         assert title_field.max_length == 200, 'Задайте максимальную длину `title` модели `Group` 200'

#         slug_field = search_field(model_fields, 'slug')
#         assert slug_field is not None, 'Добавьте уникальный адрес группы `slug` модели `Group`'
#         assert type(slug_field) == fields.SlugField, (
#             'Свойство `slug` модели `Group` должно быть `SlugField`'
#         )
#         assert slug_field.unique, 'Свойство `slug` модели `Group` должно быть уникальным'

#         description_field = search_field(model_fields, 'description')
#         assert description_field is not None, 'Добавьте описание `description` модели `Group`'
#         assert type(description_field) == fields.TextField, (
#             'Свойство `description` модели `Group` должно быть текстовым `TextField`'
#         )

#     @pytest.mark.django_db(transaction=True)
#     def test_group_create(self, user):
#         text = 'Тестовый пост'
#         author = user

#         assert Post.objects.all().count() == 0

#         post = Post.objects.create(text=text, author=author)
#         assert Post.objects.all().count() == 1
#         assert Post.objects.get(text=text, author=author).pk == post.pk

#         title = 'Тестовая группа'
#         slug = 'test-link'
#         description = 'Тестовое описание группы'

#         assert Group.objects.all().count() == 0
#         group = Group.objects.create(title=title, slug=slug, description=description)
#         assert Group.objects.all().count() == 1
#         assert Group.objects.get(slug=slug).pk == group.pk

#         post.group = group
#         post.save()
#         assert Post.objects.get(text=text, author=author).group == group
