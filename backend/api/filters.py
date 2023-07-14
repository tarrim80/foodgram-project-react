from django_filters import rest_framework as filters
from recipes.models import Ingredient, Recipe
from users.models import User


class IngredientNameFilter(filters.FilterSet):
    """Фильтр ингредиентов по названию."""

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(filters.FilterSet):
    """Множественный фильтр рецептов по параметрам запроса."""

    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )

    def filter_is_favorited(self, queryset, _, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(
                relations__user=self.request.user, relations__is_favorited=True
            )
        return queryset

    def filter_is_in_shopping_cart(self, queryset, _, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(
                relations__user=self.request.user,
                relations__is_in_shopping_cart=True,
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ("tags", "author")
