from django.contrib import admin
from django.urls import path

admin.site.site_header = 'Админ-панель Продуктового помощника'

urlpatterns = [
    path('admin/', admin.site.urls),
]
