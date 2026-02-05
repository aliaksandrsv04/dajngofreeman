from django.test import TestCase


from decimal import Decimal
from myapp.models import Product

'''Тестики'''

class ProductModelTest(TestCase):
    def test_crud_operations(self):
        product = Product.objects.create(name="Tablet", price=1000)
        self.assertEqual(Product.objects.count(), 1)

        product.price = 900
        product.save()
        self.assertEqual(Product.objects.get(pk=product.pk).price, 900)

        product.delete()
        self.assertEqual(Product.objects.count(), 0)

class ProductTests(TestCase):
    def test_price_with_vat(self):
        product = Product(name='Phone', price=Decimal('100.00'))
        self.assertEqual(product.price_with_vat, Decimal('120.00'))

    def test_apply_discount(self):
        product = Product(name='Phone', price=Decimal('500.00'))
        discounted = product.apply_discount(10)
        self.assertEqual(discounted, 450.00)

