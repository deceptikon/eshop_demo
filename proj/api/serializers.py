from django.contrib.auth.models import User, Group
from eshop.models import Product, CartContent
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description']

class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CartContent
        fields = ['product', 'product_id', 'quantity']