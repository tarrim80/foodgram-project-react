from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """
    Модель ингредиентов.
    С рецептом связано множество ингредиентов.
    """

    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Наименование ингредиента',)
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единицы измерения',
                                        help_text='Единицы измерения продукта')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Модель тегов.
    На рецепт может быть назначено несколько тегов.
    """

    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Наименование тега',
                            unique=True)

    color = ColorField(default='#FF0000',
                       unique=True,
                       verbose_name='Цветовой HEX-код',
                       help_text='Определите цвет тега')

    slug = models.SlugField(max_length=200,
                            unique=True,
                            verbose_name='Слаг',
                            help_text='Уникальный слаг')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """
    Модель рецептов. Основная сущность сервиса.
    Рецепты связаны со всеми сервисами и страницами проекта.
    """

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации',
                               help_text='Создатель публикации рецепта.')

    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Название рецепта.')

    image = models.ImageField(upload_to='images/',
                              verbose_name='Картинка',
                              help_text='Загрузите изображение.')

    text = models.TextField(verbose_name='Описание',
                            help_text='Текстовое описание приготовления блюда')

    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Список ингредиентов',
                                         help_text='Добавьте ингредиенты.')

    tags = models.ManyToManyField(Tag,
                                  through='RecipeTag',
                                  verbose_name='Список тегов',
                                  help_text='Укажите теги.')

    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления рецепта (в минутах).',
        validators=(MinValueValidator(1),)
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Дата и время вносятся атоматически',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'

    def __str__(self) -> str:
        return self.name


class RecipeTag(models.Model):
    """
    Модель связующая рецепт и  теги.
    Отношение моделей - Многие ко Многим.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            verbose_name='Тег',
                            help_text='Выберите теги.')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='recipe_tag'
            ),
        )
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return f'{self.tag}_{self.recipe}'


class RecipeIngredient(models.Model):
    """
    Модель связующая рецепт и ингредиенты.
    Модель содержит свойство `количество ингредиента`.
    Отношение моделей - Многие ко Многим.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   help_text='Выберите ингредиенты.')

    amount = models.FloatField(
        verbose_name='Количество',
        help_text='Укажите необходимое количество продукта.',
        validators=(MinValueValidator(1),)
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='recipe_ingredient'
            ),
        )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.recipe}_{ self.ingredient}'


class RecipeRelation(models.Model):
    """
    Модель связующая пользователя с рецептами посредством булевых полей
    `on_favorites_list` `on_shopping_list`.
    """
    user = models.ForeignKey(User,
                             verbose_name='пользователь',
                             help_text='Укажите пользователя',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               help_text='Выберите рецепт',
                               on_delete=models.CASCADE)
    is_favorited = models.BooleanField(
        verbose_name='В избранном',
        help_text='Отметьте, чтобы добавить в избранное',
        default=False
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='В списке покупок',
        help_text='Отметьте, чтобы добавить в список покупок',
        default=False
    )

    class Meta:
        verbose_name = 'Связи рецепта'
        verbose_name_plural = 'Связи рецептов'
        ordering = ('user', '-recipe')
        default_related_name = 'relations'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_relations'
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} - {self.recipe}'
