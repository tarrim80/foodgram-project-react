from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from recipes.models import (Ingredient, Recipe, RecipeIngredient,
                            RecipeRelation, RecipeTag, Tag)

admin.site.site_title = 'Продуктовый помощник'
admin.site.site_header = 'Продуктовый помощник'
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
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    list_per_page = 15


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    """Админ-панель рецептов"""

    list_display = ('image_tag', 'name', 'pub_date',
                    'author', 'favorite_count', 'cooking_time', 'text',)
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'text', 'tags__name', 'ingredients__name',)
    fields = (('name', 'cooking_time'), ('author', 'pub_date',), 'text',
              ('image_tag', 'image',))
    readonly_fields = ('image_tag', 'pub_date')
    inlines = (RecipeTagInline, RecipeIngredientInline)

    class Meta:
        model = Recipe

    def image_tag(self, obj) -> mark_safe:
        return mark_safe(
            f'<img src="{obj.image.url}" width="100" height="75"/>'
        )

    def favorite_count(self, obj) -> int:
        return obj.relations.filter(on_favorite_list=True).count()

    favorite_count.short_description = 'В избранном'

    image_tag.short_description = 'Миниатюра'
    image_tag.allow_tags = True


class RecipeRelationAdmin(admin.ModelAdmin):
    """Админ-панель отношений пользователя и рецепта."""
    list_display = ('user', 'recipe', 'on_favorite_list',
                    'on_shopping_list')
    list_filter = ('user', 'on_favorite_list', 'on_shopping_list')
    search_fields = ('user', 'recipe')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeRelation, RecipeRelationAdmin)
admin.site.register(Tag, TagAdmin)
