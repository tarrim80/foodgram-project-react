from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag

admin.site.site_title = 'Админ-панель Продуктового помощника'
admin.site.site_header = 'Админ-панель Продуктового помощника'
admin.site.unregister(Group)


class TagAdmin(admin.ModelAdmin):
    """Админ-панель тегов"""

    prepopulated_fields = {'slug': ('name',)}

    list_display = ('name', 'color', 'slug')
    list_editable = ('color',)
    fields = (('name', 'slug'), 'color')


class IngredientAdmin(admin.ModelAdmin):
    """Админ-панель ингредиентов"""

    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    """Админ-панель рецептов"""

    list_display = ('image_tag', 'name', 'pub_date',
                    'author', 'text', 'cooking_time')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)
    fields = (('name', 'cooking_time'), ('author', 'pub_date',), 'text',
              ('image_tag', 'image',))
    readonly_fields = ('image_tag', 'pub_date')
    inlines = (RecipeTagInline, RecipeIngredientInline)

    class Meta:
        model = Recipe

    def image_tag(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="100" height="75"/>'
        )

    image_tag.short_description = 'Миниатюра'
    image_tag.allow_tags = True


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
