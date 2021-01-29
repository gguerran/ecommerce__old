from rest_framework.permissions import BasePermission


WRITE_METHOD = ['POST']


class IsAuthenticatedOrWriteOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in WRITE_METHOD or
            request.user and request.user.is_authenticated
        )
