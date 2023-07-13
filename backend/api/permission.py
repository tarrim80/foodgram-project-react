from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdminOnly(BasePermission):
    """
    Доступно автору рецепта и администратору для изменения,
    а остальным для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user == obj.author or request.user.is_staff)
        )


class IsCreateOrAdminOnly(BasePermission):
    """Доступно администратору или авторизованному для создания."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.method == "POST"
            or request.user.is_authenticated
            and request.user.is_staff
        )


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Доступно администратору для создания, редактирования и удаления."""
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_staff
        )
