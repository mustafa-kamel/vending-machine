from rest_framework.permissions import (
    BasePermission, IsAuthenticated, SAFE_METHODS)
from .models import Roles


class IsAuthenticatedOrRegister(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST' and view.action != 'deposit':
            return True
        if (request.user.is_authenticated
            and view.action in ['deposit', 'reset']
                and request.user.role != Roles.BUYER):
            return False
        return super(
            IsAuthenticatedOrRegister, self).has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or obj.id == request.user.id:
            return True
        return False


class IsSellerAndOwner(BasePermission):
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or request.user.role == Roles.SELLER
                or (view.action == 'buy' and request.user.role == Roles.BUYER
                    )):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or obj.seller == request.user:
            return True
        return False
