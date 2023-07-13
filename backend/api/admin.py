from django.contrib import admin
from rest_framework.authtoken.admin import Token, TokenAdmin, TokenProxy

admin.site.register(Token, TokenAdmin)
admin.site.unregister(TokenProxy)
