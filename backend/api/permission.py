from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrAuthorOrReadOnly(BasePermission):
    """
    Доступно автору рецепта и администратору для изменения,
    а остальным для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            obj.author == request.user
        ) or request.user and request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    """Доступно администратору для изменения и остальным для чтения."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user and request.user.is_staff)
