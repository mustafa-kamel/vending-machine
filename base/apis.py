from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from base.models import User, Product
from base.serializers import UserSerializer, ProductSerializer
from base.permissions import (IsAuthenticatedOrRegister, IsSellerAndOwner)


class UserViewSet(DynamicModelViewSet):
    permission_classes = (IsAuthenticatedOrRegister, )
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
    ordering = ['-date_joined']

    def get_queryset(self):
        return self.queryset.filter(pk=self.request.user.pk)


class ProductViewSet(DynamicModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsSellerAndOwner,)
    serializer_class = ProductSerializer
    model = Product
    queryset = Product.objects.all()
    ordering = ['name']

    def create(self, request):
        request.data._mutable = True
        request.data['seller'] = request.user
        return super(ProductViewSet, self).create(request)
