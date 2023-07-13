from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from users.models import Subscribe, User


class UserCreateForm(UserCreationForm):
    """
    Отображение дополнительных полей
    при добавлении пользователя через админ-панель.
    """

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class UserAdmin(UserAdmin):
    """Админ-панель пользователей."""

    add_form = UserCreateForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                ),
            },
        ),
    )
    prepopulated_fields = {"username": ("first_name", "last_name")}

    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email")
    list_filter = (
        "username",
        "email",
    )
    empty_value_display = "-пусто-"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "is_staff",
                )
            },
        ),
    )


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    list_filter = ("user", "author")
    search_fields = ("user", "author")
    list_per_page = settings.PAGE_SIZE * 5


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
