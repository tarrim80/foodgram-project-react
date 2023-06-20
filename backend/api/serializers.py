from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from api.validators import username_validator
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User, Subscribe
from djoser.serializers import UserSerializer as DjoserSerializer


class UserSerializer(DjoserSerializer):
    """Сериализатор пользователей приложения."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password', 'is_subscribed')
        read_only_fields = ('id', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True}, }

    def get_is_subscribed(self, obj) -> bool:
        user = self.context.get('request').user
        return False if user.is_anonymous else Subscribe.objects.filter(
            author=obj.id, user=user).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = (
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=('ingredient', 'recipe'),
                message='Этот ингредиент уже добавлен!'
            ),
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    # author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientAmountSerializer(
        source='recipeingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')
