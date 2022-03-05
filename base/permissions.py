from rest_framework.permissions import IsAuthenticated


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
