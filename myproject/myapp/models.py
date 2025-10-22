from django.db import models


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
    image = models.ForeignKey(
        'Image',
        to_field='name',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Image(models.Model):

    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image1 = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name