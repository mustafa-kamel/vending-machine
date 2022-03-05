from django.contrib.auth.hashers import make_password
from dynamic_rest.serializers import (DynamicModelSerializer,
                                      DynamicRelationField)

from .models import User, Product


class UserSerializer(DynamicModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'deposit', 'role',
                  'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        return make_password(value)


class ProductSerializer(DynamicModelSerializer):
    seller = DynamicRelationField(UserSerializer, embed=True)

    class Meta:
        model = Product
        fields = '__all__'
