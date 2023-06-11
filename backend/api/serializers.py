from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.validators import validate_username  # noqa
from users.models import User


class UsernameMeMixin:
    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'username не может быть "me"')
        return username


class FoodgramUserSerializer(UserSerializer):
    last_name = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    email = serializers.CharField(max_length=254, required=True, validators=(
        UniqueValidator(
            queryset=User.objects.all(),
            message='email должен быть уникальным!'
        ),
    ))
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(
            validate_username,
            UniqueValidator(
                queryset=User.objects.all(),
                message='username должен быть уникальным!'
            )),
    )
    password = serializers.CharField(
        write_only=True, required=True,
        style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        read_only_fields = ('id',)


class SignUpSerializer(serializers.ModelSerializer, UsernameMeMixin):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        password = data['password']
        email = data['email']

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise serializers.ValidationError(
                        'Некорректный пароль.')
                data['user'] = user
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    'Пользователь с таким `email` не зарегистрирован.'
                )
        else:
            raise serializers.ValidationError(
                'Учётные данные не предоставлены.'
            )
        return data

    class Meta:
        model = User
        fields = ('password', 'email')
        extra_kwargs = {
            'password': {'required': True},
            'email': {'required': True}
        }
