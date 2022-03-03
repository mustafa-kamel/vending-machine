from django.db import models
from django.contrib.auth.models import AbstractUser


class Roles(models.TextChoices):
    SELLER = 'seller', 'Seller'
    BUYER = 'buyer', 'Buyer'


class User(AbstractUser):
    deposit = models.FloatField(default=0)
    role = models.CharField(
        max_length=20, choices=Roles.choices, default=Roles.BUYER)

    class Meta:
        db_table = "users"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    available = models.IntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "products"
