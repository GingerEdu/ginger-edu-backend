from rest_framework.permissions import BasePermission


class IsAuthenticatedAdmin(BasePermission):
    """
    Allows access only to authenticated admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.is_admin)
