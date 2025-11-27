from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

# User = get_user_model()

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.username



class Product(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Image(models.Model):

    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images'
    )

class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='orders'

    )
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=12)
    email = models.EmailField()

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_items'
    )