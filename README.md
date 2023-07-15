<div align="center">

# Дипломный проект
## Сайт Foodgram, «Продуктовый помощник».
</div>
<div align="center">

![Foodgram Главная страница](backend\media\github\2023-07-15_22-20-21.png)
</div>
Онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


Список продуктов реализован через pdf-файл вида:
<div align="center">

![Список продуктов](backend/media/github/shopping-list.svg)
</div>
<div align="center">

## Функциональность проекта
</div>

Все сервисы и страницы доступны для пользователей в соответствии с их правами. 
Рецепты на всех страницах сортируются по дате публикации (новые — выше).
Работает фильтрация по тегам (в том числе на странице избранного и на странице рецептов одного автора).
Работает пагинатор (в том числе при фильтрации по тегам).
Исходные данные предзагружены; добавлены тестовые пользователи и рецепты.

<div align="center">

### Для авторизованных пользователей:
</div>

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

<div align="center">

### Для неавторизованных пользователей

</div>

- Доступна главная страница.
- Доступна страница отдельного рецепта.
- Доступна и работает форма авторизации.
- Доступна и работает система восстановления пароля.
- Доступна и работает форма регистрации.


<div align="center">

### Администратор и админ-зона
</div>

- Все модели выведены в админ-зону.
- Для модели пользователей включена фильтрация по имени и email.
- Для модели рецептов включена фильтрация по названию, автору и тегам.
- На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное.
- Для модели ингредиентов включена фильтрация по названию.

<div align="center">

## Документация API
</div>

Полробная документация по работе API сервиса доступна по адресу: [\<hostname\>/api/docs/](http://tarrim80.hopto.org/api/docs/)

<div align="center">

## Подстановочные (фиктивные) данные
</div>

В репозитории доступна папка ```mock_data``` с файлами содержащими данные о рецептах, спарсенных с сайта [![FOOD.RU](https://img.shields.io/badge/FOOD.RU-FFDE00?style=for-the-badge/)](https://food.ru/)  
Данные распространяются только в ознакомительных целях. Все права принадлежат правообладателям.  
Подгрузка данных при первом запуске произойдет автоматически. В остальных случаях подгрузить данные можно командой:

```
python manage.py loaddata mock_data/*
```
<div align="center">

### Используемые технологии:

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python&logoColor=FFFFFF)](https://www.python.org/)&nbsp;&nbsp;[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django&logoColor=FFFFFF)](https://www.djangoproject.com/)&nbsp;&nbsp;[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework&logoColor=FFFFFF)](https://www.django-rest-framework.org/)&nbsp;&nbsp;[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL&logoColor=FFFFFF)](https://www.postgresql.org/)&nbsp;&nbsp;[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX&logoColor=FFFFFF)](https://nginx.org/ru/)&nbsp;&nbsp;[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn&logoColor=FFFFFF)](https://gunicorn.org/)&nbsp;&nbsp;[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker&logoColor=FFFFFF)](https://www.docker.com/)&nbsp;&nbsp;
![github](https://img.shields.io/badge/github-464646?style=flat-square&logo=github&logoColor=FFFFFF)&nbsp;&nbsp;[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud&logoColor=FFFFFF)](https://cloud.yandex.ru/)&nbsp;&nbsp;[![Beautiful Soup](https://img.shields.io/badge/-Beautiful%20Soup-464646?style=flat-square&logo=Beautiful%20Soup)](https://www.crummy.com/software/BeautifulSoup/) [![FPDF2](https://img.shields.io/badge/-FPDF2-464646?style=flat-square&logo=FPDF2)](https://pyfpdf.github.io/fpdf2/)&nbsp;&nbsp;[![django-colorfiels](https://img.shields.io/badge/-django--colorfield-464646?style=flat-square&logo=django--colorfield)](https://github.com/fabiocaccamo/django-colorfield)



</div>
<div align="center">

## Локальный запуск  
</div>
Для локального запуска склонируйте репозиторий на свой компьютер:

```
git@github.com:tarrim80/foodgram-project-react.git
```

необходимы установленные [_Docker_](https://docs.docker.com/engine/install/)
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

<div align="center">

```
username - admin
email - admin@f.fake
password - 123
```
</div>

У всех загруженных в БД фиктивных пользователей пароль - 123

Для самостоятельных миграций и подгрузки статики потребуются команды:

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
sudo docker compose exec backend cp -r /app/collected_static/. /foodgram_backend_static/static/
```
<div align="center">

## Временное размещение
</div>

В рамках прохождения курса обучения проект временно размещен на сервере ```Yandex Cloud``` и доступен по адресу:

[https://tarrim80.hopto.org/](https://tarrim80.hopto.org/)

---


Удачных разработок!!!

<div align="center">

### Выполнено в рамках прохождения курса "Python-разработчик плюс" на ["Яндекс Практикум"](https://practicum.yandex.ru/)
</div>
