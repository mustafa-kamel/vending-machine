from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Roles


class IsAuthenticatedOrRegister(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(
            IsAuthenticatedOrRegister, self).has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if obj.id != request.user.id:
            return False
        return True


class IsSellerAndOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.role != Roles.SELLER:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if obj.seller != request.user:
            return False
        return True
