

#0 Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from decimal import Decimal
from myapp.models import Product, CustomUser
from rest_framework import status
from rest_framework.test import APITestCase



# class ProductTests(TestCase):
#     def test_price_with_vat(self):
#         product = Product(name='Phone', price=Decimal('100.00'))
#         self.assertEqual(product.price, Decimal('100.00'))

# class ProductIntegrationTest(APITestCase):
#     def test_create_product(self):
#         data = {'name' : 'Laptop', 'price': '200.00'}
#         response = self.client.post('/api/products/create', data)
#         print(response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Product.objects.filter(name = 'Laptop').exists())
# class ProductListTest(APITestCase):
#     def test_get_products(self):
#         Product.objects.create(name = 'Phone', price = '500.00')
#         response = self.client.get('/api/products/')
#         print(TestCase.__mro__)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Phone', str(response.data))


class ProductViewTest(TestCase):
    # def test_product_detail_test(self):
    #     product = Product.objects.create(name = "Mac", price = '1000.0')
    #     response = self.client.get(f'/api/products/detail/{product.id}')
    #     self.assertEqual(response.status_code, 403)
    #     print(str(response.data))
    # def test_redirect_after_register(self):
    #     response = self.client.post('/register/',{
    #         'username': 'user',
    #         'password':'123',
    #         'password2' : '123',
    #         'email' : '1@gmail.com',
    #         'phone' : '+37523123134',
    #         'first_name':'sx',
    #         'last_name': 'ax'
    #     })
    #     try:
    #         print(response.context['form'].errors)
    #     except:
    #         pass
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_template(self):
    #     response = self.client.get('/')
    #     self.assertContains(response, "Список товаров")

    def test_login(self):
        product = Product.objects.create(name='Phone', price='500.00')
        user = CustomUser.objects.create(username = 'ad', password = '123')
        self.client.force_login(user)
        response = self.client.get(f'/api/products/detail/{product.id}')
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user(self):
        product = Product.objects.create(name='Phone', price='500.00')
        response = self.client.get(f'/api/products/detail/{product.id}')
        self.assertEqual(response.status_code, 403)