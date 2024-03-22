from rest_framework import permissions


class IsAdminOrSuperuserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            ((not request.user.is_anonymous) and (
                request.user.is_superuser
                or request.user.role == 'admin'))
            or request.method in permissions.SAFE_METHODS
        )
