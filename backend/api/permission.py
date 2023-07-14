from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrCreatorOrAdminOnly(BasePermission):
    """
    Доступно администратору для любых действий,
    автору рецепта для изменения собственного рецепта,
    зарегистрированному пользователю для создания рецепта,
    а также всем остальным для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            (request.user.is_authenticated and request.method == "POST")
            or (
                request.user.is_authenticated
                and (request.user == obj.author or request.user.is_staff)
            )
        )


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Доступно администратору для создания, редактирования и удаления."""
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_staff
        )
