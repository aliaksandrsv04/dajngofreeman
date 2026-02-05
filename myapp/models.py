from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

# User = get_user_model()
''' Делаю своего юзера с телефоном '''
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.username


#Продукт с внешним полем под категорию
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

    @property
    def price_with_vat(self):
        """Возвращает цену с НДС (20%)"""
        if self.price:
            vat_rate = Decimal('1.20')  # НДС 20%
            return self.price * vat_rate
        return Decimal('0.00')

    # 2. Метод apply_discount
    def apply_discount(self, discount_percent):
        """
        Применяет скидку в процентах
        Args:
            discount_percent: процент скидки (например, 10 для 10%)
        Returns:
            Цена после скидки
        """
        if self.price:
            discount_decimal = Decimal(str(discount_percent)) / Decimal('100')
            discount_amount = self.price * discount_decimal
            return float(self.price - discount_amount)  # Возвращаем float как в тесте
        return 0.0


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Картинки соединенные с продуктами - картинок может быть несколько на один продукт
class Image(models.Model):

    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images'
    )
#Заказ с внешним полем под юзера
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

#Объединяю продукт с заказом
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