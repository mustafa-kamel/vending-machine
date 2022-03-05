from dynamic_rest.serializers import (DynamicModelSerializer)

from .models import User


class UserSerializer(DynamicModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'deposit', 'role',
                  'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
