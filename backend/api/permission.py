from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Доступно автору рецепта для изменения и остальным для чтения."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    """Доступно администратору для изменения и остальным для чтения."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user and request.user.is_staff)
