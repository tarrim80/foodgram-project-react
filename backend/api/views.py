import os

from api.filters import IngredientNameFilter, RecipeFilter
from api.pagination import PageNumberPaginationLimit
from api.permission import IsAdminOrReadOnly, IsAuthorOrCreatorOrAdminOnly
from api.serializers import (
    IngredientSerializer,
    RecipeMinifiedSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    TagSerializer,
)
from api.services import create_shopping_file
from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserViewSet
from recipes.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeRelation,
    Tag,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Subscribe


class UserViewSet(DjoserViewSet):
    """Представление пользователей."""

    pagination_class = PageNumberPaginationLimit

    def get_recipes_limit(self):
        """Получение ограничения на количество рецептов из запроса."""
        recipes_limit = self.request.query_params.get("recipes_limit", None)
        try:
            return int(recipes_limit) if recipes_limit else None
        except ValueError:
            return None

    @action(detail=True, methods=("post", "delete"))
    def subscribe(self, request, id):
        """Подписка/отписка на автора рецептов."""
        user = request.user
        author = self.get_object()
        if user == author:
            return Response(
                {"errors": "Ошибка подписки/отписки на самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscribe, create_status = Subscribe.objects.get_or_create(
            user=user, author=author
        )
        if request.method == "POST" and create_status:
            serialiser = SubscribeSerializer(
                subscribe, context={"recipes_limit": self.get_recipes_limit()}
            )
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE" and not create_status:
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"errors": "Ошибка подписки/отписки на автора"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False)
    def subscriptions(self, request):
        """Представление списка подписок."""
        user = request.user
        pages = self.paginate_queryset(Subscribe.objects.filter(user=user))
        serializer = SubscribeSerializer(
            pages,
            context={"recipes_limit": self.get_recipes_limit()},
            many=True,
        )
        return self.get_paginated_response(serializer.data)


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientNameFilter


class RecipeViewSet(ModelViewSet):
    """Представление рецептов."""

    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrCreatorOrAdminOnly,)
    pagination_class = PageNumberPaginationLimit
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = RecipeFilter
    search_fields = ("name", "text", "ingredients__name", "tags__name")
    lookup_field = "id"

    def get_queryset(self):
        """Определение списка рецептов."""

        queryset = Recipe.objects.select_related("author").prefetch_related(
            "tags", "relations"
        )
        return queryset

    def relation_delete(self, relation):
        """Удаление пустых связей."""
        if not relation.is_favorited and not relation.is_in_shopping_cart:
            relation.delete()

    @action(
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def favorite(self, request, id):
        """Добавление/удаление рецепта в избранное."""

        recipe = self.get_object()
        user = self.request.user
        if recipe.author == user:
            return Response(
                {"errors": "Нельзя добавить в избранное свой рецепт."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        relation, _ = RecipeRelation.objects.get_or_create(
            recipe=recipe, user=user
        )
        field = relation.is_favorited
        if self.request.method == "POST":
            if field:
                return Response(
                    {"errors": "Рецепт уже был добавлен в избранное."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                relation.is_favorited = True
                relation.save()
                return Response(
                    RecipeMinifiedSerializer(recipe).data,
                    status=status.HTTP_201_CREATED,
                )
        elif self.request.method == "DELETE":
            if not field:
                return Response(
                    {"errors": "Рецепт уже был удалён из избранного."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                relation.is_favorited = False
                relation.save()
                self.relation_delete(relation)
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"errors": "Ошибка добавления/удаления рецепта в избранное"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def shopping_cart(self, request, id):
        """Добавление/удаление рецепта в список покупок."""

        recipe = self.get_object()
        user = self.request.user

        relation, _ = RecipeRelation.objects.get_or_create(
            recipe=recipe, user=user
        )
        field = relation.is_in_shopping_cart
        if self.request.method == "POST":
            if field:
                return Response(
                    {"errors": "Рецепт уже был добавлен в список покупок."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                relation.is_in_shopping_cart = True
                relation.save()
                return Response(
                    RecipeMinifiedSerializer(recipe).data,
                    status=status.HTTP_201_CREATED,
                )
        elif self.request.method == "DELETE":
            if not field:
                return Response(
                    {"errors": "Рецепт уже был удалён из списка покупок."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                relation.is_in_shopping_cart = False
                relation.save()
                self.relation_delete(relation)
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    "errors": "Ошибка добавления/удаления "
                    "рецепта в список покупок."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        methods=("get",), permission_classes=(IsAuthenticated,), detail=False
    )
    def download_shopping_cart(self, request):
        """Скачивание списка покупок."""
        user = request.user
        queryset = (
            RecipeIngredient.objects.filter(
                recipe__relations__user=user,
                recipe__relations__is_in_shopping_cart=True,
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(Sum("amount"))
        )

        for item in queryset:
            item["amount__sum"] = f"{item['amount__sum']:g}"

        fp = settings.SHOPPING_LIST_FILE_PARAMS.get("FILE_DOWNLOAD")
        file = create_shopping_file(queryset)
        return FileResponse(file, status=status.HTTP_200_OK, **fp)

    def perform_create(self, serializer):
        """Передача текущего пользователя в качестве автора рецепта."""
        if self.request.user.is_anonymous:
            raise PermissionDenied(
                "Зарегистрируйтесь, чтоб разместить рецепт."
            )
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Удаление рецепта и его картинки."""
        obj = self.get_object()
        if obj.image:
            os.remove(obj.image.path)
        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
