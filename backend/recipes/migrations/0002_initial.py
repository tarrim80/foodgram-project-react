# Generated by Django 3.2.20 on 2023-07-13 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reciperelation",
            name="user",
            field=models.ForeignKey(
                help_text="Укажите пользователя",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="recipeingredient",
            name="ingredient",
            field=models.ForeignKey(
                help_text="Выберите ингредиенты.",
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AddField(
            model_name="recipeingredient",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.recipe",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                help_text="Создатель публикации рецепта.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор публикации",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                help_text="Добавьте ингредиенты.",
                related_name="recipes",
                through="recipes.RecipeIngredient",
                to="recipes.Ingredient",
                verbose_name="Список ингредиентов",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                help_text="Укажите теги.",
                related_name="recipes",
                through="recipes.RecipeTag",
                to="recipes.Tag",
                verbose_name="Список тегов",
            ),
        ),
        migrations.AddConstraint(
            model_name="recipetag",
            constraint=models.UniqueConstraint(
                fields=("recipe", "tag"), name="recipe_tag"
            ),
        ),
        migrations.AddConstraint(
            model_name="reciperelation",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_recipe_relations"
            ),
        ),
        migrations.AddConstraint(
            model_name="recipeingredient",
            constraint=models.UniqueConstraint(
                fields=("recipe", "ingredient"), name="recipe_ingredient"
            ),
        ),
    ]
