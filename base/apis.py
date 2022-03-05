from dynamic_rest.viewsets import DynamicModelViewSet

from base.models import User
from base.serializers import UserSerializer
from base.permissions import (IsAuthenticatedOrRegister)


class UserViewSet(DynamicModelViewSet):
    permission_classes = (IsAuthenticatedOrRegister, )
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
    ordering = ['-date_joined']
