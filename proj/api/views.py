import ast
from django.contrib.auth.models import User, Group
from eshop.models import Product, Cart, CartContent
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from .serializers import UserSerializer, GroupSerializer, ProductSerializer, CartSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ProductView(APIView):
    """
    List all products
    """
    queryset = Product.objects.all()

    def get(self, request):
        prods = Product.objects.all()
        serializer = ProductSerializer(prods, many=True, context={'request': request})
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    """
    We retrieve our products with viewset
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    Here we get cart records and add to cart
    """
    queryset = CartContent.objects.all()
    serializer_class = CartSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = 1
        cart = Cart.objects.get(user_id=self.user_id)
        self.queryset = CartContent.objects.filter(cart=cart)

    @action(detail=True, methods=['put'], name='Add to cart')
    def put(self, request, pk=None):
        """recording to cart"""
        print(request.body, pk)
        data = { 'test': 'testdata' }
        if request.body:
            request_data = ast.literal_eval(request.body.decode('utf-8'))
            cart = Cart.objects.get(user_id=self.user_id)
            prod = Product.objects.get(id=request_data['product'])
            cart_data = []
            try:
                cart_record = CartContent.objects.get(cart_id=cart.id, product_id=prod.id)
                cart_record.quantity = cart_record.quantity + 1
            except ObjectDoesNotExist:
                cart_record = CartContent(
                    product=prod,
                    cart=cart,
                    quantity=1
                )
            finally:
                cart_record.save()
                cart_data = CartContent.objects.filter(cart=cart)
                # serialized_cart = CartSerializer(cart_data, many=True, context={'request': request})
                serialized_cart = serializers.serialize('json', cart_data)
                data = { 'status': 'Added to cart', 'data': serialized_cart }
        return Response(data)
