from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
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

    allowed_deposits = [5, 10, 20, 50, 100]

    def get_queryset(self):
        return self.queryset.filter(pk=self.request.user.pk)

    @action(methods=['post'], detail=False)
    def deposit(self, request, *args, **kwargs):
        deposit = int(request.data.get('deposit'))
        if deposit not in self.allowed_deposits:
            raise ParseError(
                {"detail": "Deposits allowed are: %s."
                 % ', '.join(map(lambda x: str(x), self.allowed_deposits))})
        request.user.deposit += deposit
        request.user.save()
        return Response(self.get_serializer(request.user).data)

    @action(methods=['get'], detail=False)
    def reset(self, request, *args, **kwargs):
        if request.user.deposit not in self.allowed_deposits:
            deposit = 0
            for val in self.allowed_deposits:
                if request.user.deposit < val:
                    break
                deposit = val
            request.user.deposit = deposit
        request.user.save()
        return Response(self.get_serializer(request.user).data)


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
