from django.shortcuts import get_object_or_404

from djoser.serializers import SetPasswordSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import FoodgramUserSerializer, SignUpSerializer  # noqa
from users.models import User


class GetTokenUser(CreateAPIView):
    """Выдача токена аутентификации."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'auth_token': str(token),
        }, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """Представление пользователей."""
    queryset = User.objects.all()
    serializer_class = FoodgramUserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'id'

    @action(["post"], detail=False, permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        obj = get_object_or_404(User, email=request.user.email)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
