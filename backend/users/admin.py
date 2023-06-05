from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCreateForm(UserCreationForm):
    """
    Отображение дополнительных полей
    при добавлении пользователя через админ-панель.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserAdmin(UserAdmin):
    """ Админ-панель пользователей """
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name',
                       'last_name',
                       'username',
                       'email',
                       'password1',
                       'password2',
                       'is_staff'),
        }),
    )
    prepopulated_fields = {'username': ('first_name', 'last_name')}

    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password',
         'first_name', 'last_name', 'is_staff')}),
    )


admin.site.register(User, UserAdmin)
