import base64

from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db.models import F
from djoser.serializers import UserSerializer as DjoserSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from rest_framework.validators import ValidationError
from users.models import Subscribe, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class UserSerializer(DjoserSerializer):
    """Сериализатор пользователей приложения."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed",
        )
        read_only_fields = ("id", "is_subscribed")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def get_is_subscribed(self, obj) -> bool:
        user = self.context.get("request").user
        return (
            False
            if user.is_anonymous
            else Subscribe.objects.filter(author=obj.id, user=user).exists()
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")
        read_only_fields = ("__all__",)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")
        read_only_fields = ("__all__",)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов (полный)."""

    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                limit_value=1,
                message="Время приготовления должно быть больше или равно 1",
            ),
        )
    )
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        """Получение списка ингредиентов с количеством для рецепта."""
        return obj.ingredients.values(
            "id",
            "name",
            "measurement_unit",
            amount=F("recipeingredient__amount"),
        )

    def get_realtions_field(self, obj, field_name):
        """Проверка значений полей связи рецепта с пользователем."""
        user = self.context.get("request").user
        try:
            relation = obj.relations.get(user=user)
        except Exception:
            return False
        return getattr(relation, field_name)

    def get_is_favorited(self, obj):
        """Рецепт находится в избранном."""
        return self.get_realtions_field(obj, field_name="is_favorited")

    def get_is_in_shopping_cart(self, obj):
        """Рецепт находится в списке покупок."""
        return self.get_realtions_field(obj, field_name="is_in_shopping_cart")

    def recipe_ingredient_create(self, ingredients, recipe):
        """Формирование связи рецепта и ингредиентов."""

        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )

    def validate(self, data):
        """Проверки данных передаваемых в запросе."""

        validation_data = self.initial_data

        tags_data = validation_data.pop("tags")
        if not tags_data:
            raise ValidationError("Рецепт должен содержать тэги")
        tags_int = all(isinstance(tag_id, int) for tag_id in tags_data)
        if not tags_int:
            raise ValidationError("Тэги содержат недопустимые данные")
        data["tags"] = tags_data

        ingredients = self.initial_data.get("ingredients")
        if not ingredients:
            raise ValidationError("Рецепт должен содержать ингредиенты")
        ingredients_valid = []
        for ingredient in ingredients:
            ing_id = ingredient.get("id")
            ing_exists = Ingredient.objects.filter(id=ing_id).exists()
            if not ing_exists:
                raise ValidationError("Такого ингредиента нет в базе")
            ing_amount = ingredient.get("amount")
            try:
                ing_amount = float(ing_amount)
            except ValueError:
                raise ValidationError(
                    "Ингредиенты содержат недопустимые данные"
                )
            if ing_amount < 1:
                raise ValidationError(
                    "Убедитесь, что это значение больше, либо равно единице"
                )
            ingredients_valid.append({"id": ing_id, "amount": ing_amount})
        if not ingredients_valid:
            raise ValidationError("Проверьте ингредиенты")
        data["ingredients"] = ingredients_valid

        return data

    def create(self, validated_data):
        """Создание рецепта."""
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.recipe_ingredient_create(recipe=recipe, ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        """Обновление рецепта."""
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )

        if "image" in validated_data:
            image = validated_data.get("image")
            instance.image.save(image.name, image, save=True)

        tags_data = validated_data.get("tags")
        if tags_data:
            tags = Tag.objects.filter(id__in=tags_data)
            instance.tags.set(tags)

        ingredients = validated_data.get("ingredients")
        if ingredients:
            RecipeIngredient.objects.filter(recipe=instance).delete()
        self.recipe_ingredient_create(recipe=instance, ingredients=ingredients)
        instance.save()
        return instance


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов (уменьшенный)."""

    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("__all__",)


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = ("__all__",)

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = self.context.get("recipes_limit")
        queryset = obj.author.recipes.all()[:recipes_limit]
        return RecipeMinifiedSerializer(queryset, many=True).data
