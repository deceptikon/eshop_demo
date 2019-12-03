from django.db import models
from django.conf import settings
from datetime import datetime
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = settings.AUTH_USER_MODEL


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'products_category',
            kwargs = {
                'slug': self.slug
            }
        )

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Cart(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    products = models.ManyToManyField(Product, through='CartContent')
    total_cost = models.IntegerField()
    session_key = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class CartContent(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Order(Cart):
    ordered_at = models.DateTimeField(default=datetime.now)
