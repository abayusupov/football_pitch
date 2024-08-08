from rest_framework.permissions import BasePermission, IsAdminUser

class IsPitchOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_staff):
            return True
        return bool(request.user and request.user.is_owner)