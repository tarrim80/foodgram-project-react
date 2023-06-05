import re

import pytest
# from django.contrib.admin.sites import site
from django.db.models import fields
# from django.template.loader import get_template, select_template


try:
    from users.models import User
except ImportError:
    assert False, 'Не найдена модель User'

# try:
#     from recipes.models import Recipe
# except ImportError:
#     assert False, 'Не найдена модель Recipe'

# try:
#     from recipes.models import Ingredient
# except ImportError:
#     assert False, 'Не найдена модель Ingredient'

# try:
#     from recipes.models import Tag
# except ImportError:
#     assert False, 'Не найдена модель Tag'


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


class TestUser:

    def test_user_model(self):
        model_fields = User._meta.fields
        first_name_field = search_field(model_fields, 'first_name')
        assert not first_name_field.blank, (
            'Свойство `first_name` модели `User` '
            'не должно иметь атрибута `blank=True`'
        )
        last_name_field = search_field(model_fields, 'last_name')
        assert not last_name_field.blank, (
            'Свойство `last_name` модели `User` '
            'не должно иметь атрибута `blank=True`'
        )
        email_field = search_field(model_fields, 'email')
        assert not email_field.blank, (
            'Свойство `email` модели `User` '
            'не должно иметь атрибута `blank=True`'
        )
        assert email_field.db_index, (
            'Свойство `email` модели `User` '
            'должно иметь атрибут `db_index=True`'
        )
        is_staff_field = search_field(model_fields, 'is_staff')
        assert is_staff_field.verbose_name == 'администратор', (
            'Свойство `is_staff` модели `User` '
            'должно иметь атрибут `verbose_name == `администратор`'
        )

#     @pytest.mark.django_db(transaction=True)
#     def test_post_create(self, user):
#         text = 'Тестовый пост'
#         author = user

#         assert Post.objects.all().count() == 0

#         post = Post.objects.create(text=text, author=author)
#         assert Post.objects.all().count() == 1
#         assert Post.objects.get(text=text, author=author).pk == post.pk

#     def test_post_admin(self):
#         admin_site = site

#         assert Post in admin_site._registry, 'Зарегистрируйте модель `Post` в админской панели'

#         admin_model = admin_site._registry[Post]

#         assert 'text' in admin_model.list_display, (
#             'Добавьте `text` для отображения в списке модели административного сайта'
#         )
#         assert 'pub_date' in admin_model.list_display, (
#             'Добавьте `pub_date` для отображения в списке модели административного сайта'
#         )
#         assert 'author' in admin_model.list_display, (
#             'Добавьте `author` для отображения в списке модели административного сайта'
#         )
#         assert 'group' in admin_model.list_display, (
#             'Добавьте `group` для отображения в списке модели административного сайта'
#         )
#         assert 'pk' in admin_model.list_display, (
#             'Добавьте `pk` для отображения в списке модели административного сайта'
#         )
#         assert 'text' in admin_model.search_fields, (
#             'Добавьте `text` для поиска модели административного сайта'
#         )

#         assert 'group' in admin_model.list_editable, (
#             'Добавьте `group` в поля доступные для редактирования в модели административного сайта'
#         )

#         assert 'pub_date' in admin_model.list_filter, (
#             'Добавьте `pub_date` для фильтрации модели административного сайта'
#         )

#         assert hasattr(admin_model, 'empty_value_display'), (
#             'Добавьте дефолтное значение `-пусто-` для пустого поля'
#         )
#         assert admin_model.empty_value_display == '-пусто-', (
#             'Добавьте дефолтное значение `-пусто-` для пустого поля'
#         )


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
