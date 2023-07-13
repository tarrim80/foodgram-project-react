from django_filters import rest_framework as filters
from recipes.models import Ingredient


class IngredientNameFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ("name",)
