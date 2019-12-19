from django.contrib.auth.models import User, Group
from eshop.models import Product
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, ProductSerializer


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