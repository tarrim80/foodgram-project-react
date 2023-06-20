from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.pagination import LimitPageNumberPagination
from api.permission import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerializer)
from recipes.models import Ingredient, Recipe, Tag


class UserViewSet(DjoserViewSet):
    """Представление пользователей."""
    pagination_class = LimitPageNumberPagination


class TagViewSet(ReadOnlyModelViewSet):
    """Представление тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Представление ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(ModelViewSet):
    """Представление рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAdminOrReadOnly)
    pagination_class = LimitPageNumberPagination
