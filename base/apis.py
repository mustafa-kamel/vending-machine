from django.shortcuts import get_object_or_404
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from base.models import User, Product
from base.serializers import UserSerializer, ProductSerializer
from base.permissions import (IsAuthenticatedOrRegister, IsSellerAndOwner)


allowed_deposits = [5, 10, 20, 50, 100]


def get_nearest_allowed_deposit(user_deposit):
    allowed_deposit = 0
    for val in allowed_deposits:
        if user_deposit < val:
            break
        allowed_deposit = val
    return allowed_deposit


class UserViewSet(DynamicModelViewSet):
    permission_classes = (IsAuthenticatedOrRegister, )
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
    ordering = ['-date_joined']

    def get_queryset(self):
        return self.queryset.filter(pk=self.request.user.pk)

    @action(methods=['post'], detail=False)
    def deposit(self, request, *args, **kwargs):
        deposit = request.data.get('deposit')
        if not deposit:
            raise ParseError({'deposit': 'This field is required.'})
        deposit = int(deposit)
        if deposit not in allowed_deposits:
            raise ParseError(
                {"detail": "Deposits allowed are: %s."
                 % ', '.join(map(lambda x: str(x), allowed_deposits))})
        request.user.deposit += deposit
        request.user.save()
        return Response(self.get_serializer(request.user).data)

    @action(methods=['get'], detail=False)
    def reset(self, request, *args, **kwargs):
        if request.user.deposit not in allowed_deposits:
            request.user.deposit = get_nearest_allowed_deposit(
                request.user.deposit)
        request.user.save()
        return Response(self.get_serializer(request.user).data)


class ProductViewSet(DynamicModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsSellerAndOwner,)
    serializer_class = ProductSerializer
    model = Product
    queryset = Product.objects.all()
    ordering = ['name']

    def create(self, request):
        if hasattr(request.data, '_mutable'):
            request.data._mutable = True
        request.data['seller'] = request.user
        return super(ProductViewSet, self).create(request)

    def validate_request_data(self):
        if 'product' not in self.request.data:
            raise ValidationError({'product': 'This field is required.'})
        if 'amount' not in self.request.data:
            raise ValidationError({'amount': 'This field is required.'})

    def check_product_amount_and_price(self, product):
        amount = int(self.request.data.get('amount'))
        if amount > product.available:
            raise ParseError(
                {'detail': 'No enough amount of this product available.'})
        if amount * product.price > self.request.user.deposit:
            raise ParseError({'detail': 'You don\'t have enough balance.'})

    def make_transaction(self, product):
        amount = int(self.request.data.get('amount'))
        product.available -= amount
        product.save()
        total_price = amount * product.price
        self.request.user.deposit -= total_price
        self.request.user.save()
        return total_price

    @action(methods=['post'], detail=False)
    def buy(self, request, *args, **kwargs):
        self.validate_request_data()
        product = get_object_or_404(
            self.get_queryset(), pk=request.data.get('product'))
        self.check_product_amount_and_price(product)

        response = {'total': self.make_transaction(product)}
        change = get_nearest_allowed_deposit(request.user.deposit)
        if change:
            response['change'] = change
        return Response(response)
