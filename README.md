
# Дипломный проект
## Сайт Foodgram, «Продуктовый помощник».

Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Функциональность проекта
Все сервисы и страницы доступны для пользователей в соответствии с их правами. 
Рецепты на всех страницах сортируются по дате публикации (новые — выше).
Работает фильтрация по тегам (в том числе на странице избранного и на странице рецептов одного автора).
Работает пагинатор (в том числе при фильтрации по тегам).
Исходные данные предзагружены; добавлены тестовые пользователи и рецепты.
### Для авторизованных пользователей:
- Доступна главная страница.
- Доступна страница другого пользователя.
- Доступна страница отдельного рецепта.
- Доступна страница «Мои подписки».
-  Можно подписаться и отписаться на странице рецепта.
- Можно подписаться и отписаться на странице автора.
- При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.
Доступна страница «Избранное».
- На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.
- На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.
- Доступна страница «Список покупок».
- На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.
- Есть возможность выгрузить файл  .pdf с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».
- Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.
- Доступна страница «Создать рецепт».
- Есть возможность опубликовать свой рецепт.
- Есть возможность отредактировать и сохранить изменения в своём рецепте.
- Есть возможность удалить свой рецепт.
- Доступна и работает форма изменения пароля.
- Доступна возможность выйти из системы (разлогиниться).
### Для неавторизованных пользователей
- Доступна главная страница.
- Доступна страница отдельного рецепта.
- Доступна и работает форма авторизации.
- Доступна и работает система восстановления пароля.
- Доступна и работает форма регистрации.

### Администратор и админ-зона
Все модели выведены в админ-зону.
Для модели пользователей включена фильтрация по имени и email.
Для модели рецептов включена фильтрация по названию, автору и тегам.
На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное.
Для модели ингредиентов включена фильтрация по названию.

## Документация API
Полробная документация по работе API сервиса будет доступна после запуска по адресу: [localhost/api/docs/](http://localhost/api/docs/)

## Подстановочные (фиктивные) данные
В репозитории доступна папка ```mock_data``` с файлами содержащими данные о рецептах, спарсенных с сайта [food.ru](https://food.ru). Данные распространяются только в ознакомительных целях. Все права принадлежат правообладателям. Подгрузка данных при первом запуске произойдет автоматически. В остальных случаях подгрузить данные можно командой:

```
python manage.py loaddata mock_data/*
```


## Локальный запуск  
Для локального запуска необходимы установленные [_Docker_](https://docs.docker.com/engine/install/)
и [_Docker Compose_](https://docs.docker.com/compose/install/)
Далее перейти в основную директорию проекта _foodgram-project-react_ 
```
cd foodgram-project-react
```
и выполнить команды:

```
sudo docker compose down
```
```
sudo docker compose up -d
```

При запуске проекта автоматически выполнятся миграции и соберётся статика. Кроме того, при первоначальном запуске автоматически в БД загрузятся фиктивные данные для тестирования работы. В том числе создастся Суперпользователь с параметрами:

```
username - admin
email - admin@f.fake
password - 123
```
У всех загруженных в БД фиктивных пользователей пароль - 123

Для самостоятельных действий потребуются команды:

Выполнить миграции:
```
sudo docker compose exec backend python manage.py migrate
```
Собрать статику:
```
sudo docker compose exec backend python manage.py collectstatic
```
Скопировать собранную статику:
```
sudo docker compose exec backend cp -r /app/collected_static/. /kittygram_backend_static/static/
```

---
### Выполнено в рамках прохождения курса "Python-разработчик плюс" на ["Яндекс Практикум"](https://practicum.yandex.ru/)
