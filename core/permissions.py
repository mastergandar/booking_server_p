from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):

    def _is_superuser(self, request):
        try:
            res = request.user.is_authenticated and request.user.is_superuser
        except Exception:
            pass
        else:
            if res:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        return self._is_superuser(request)

    def has_permission(self, request, view):
        return self._is_superuser(request)


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
