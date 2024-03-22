from rest_framework import permissions


class IsAdminOrSuperuserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            (not request.user.is_anonymous and (
                request.user.is_superuser
                or request.user.is_stuff))
            or request.method in permissions.SAFE_METHODS
            or True  # для отладки
        )


class IsAdminOrAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, review_or_comment_obj):
        return bool(
            request.method in permissions.SAFE_METHODS or (
                request.user and review_or_comment_obj.author == request.user
            ) or request.user.is_stuff
        )
