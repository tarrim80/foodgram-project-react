from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.template.defaultfilters import truncatewords
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
    list_per_page = settings.PAGE_SIZE * 5


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    raw_id_fields = ('ingredient',)


class RecipeAdmin(admin.ModelAdmin):
    """Админ-панель рецептов"""

    list_display = ('image_tag', 'name', 'pub_date',
                    'author', 'favorite_count', 'cooking_time', 'short_text',)
    list_display_links = ('image_tag', 'name',)
    list_select_related = ('author',)
    list_filter = ('tags', 'author', 'name')
    search_fields = ('name', 'text', 'tags__name', 'ingredients__name',)
    fields = (('name', 'cooking_time'), ('author', 'pub_date',), 'text',
              ('image_tag', 'image',))
    readonly_fields = ('image_tag', 'pub_date')
    inlines = (RecipeTagInline, RecipeIngredientInline,)
    save_on_top = True
    list_per_page = settings.PAGE_SIZE
    raw_id_fields = ('author',)

    class Meta:
        model = Recipe

    def image_tag(self, obj) -> mark_safe:
        """Вывод в админ-панель миниатюры изображения к рецепту."""
        return mark_safe(
            f'<img src="{obj.image.url}" width="100" height="75"/>'
        )
    image_tag.short_description = 'Миниатюра'
    image_tag.allow_tags = True

    def favorite_count(self, obj) -> int:
        """Вывод в админ-панель количество добавлений рецепта в избранное."""
        return obj.relations.filter(is_favorited=True).count()
    favorite_count.short_description = 'В избранном'

    def short_text(self, obj) -> str:
        """Вывод в админ-панель сокращённого до 10 слов описания рецепта."""
        return truncatewords(obj.text, 10)
    short_text.short_description = 'Краткое описание'


class RecipeRelationAdmin(admin.ModelAdmin):
    """Админ-панель отношений пользователя и рецепта."""
    list_display = ('user', 'recipe', 'is_favorited',
                    'is_in_shopping_cart')
    list_filter = ('user', 'is_favorited', 'is_in_shopping_cart')
    search_fields = ('user', 'recipe')
    list_per_page = settings.PAGE_SIZE * 5
    list_select_related = ('user',)
    raw_id_fields = ('user', 'recipe')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeRelation, RecipeRelationAdmin)
admin.site.register(Tag, TagAdmin)
