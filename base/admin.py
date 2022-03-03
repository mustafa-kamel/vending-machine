from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('seller',)
    list_display = ('name', 'price', 'available', 'seller')


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
