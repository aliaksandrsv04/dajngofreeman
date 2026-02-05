import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from faker import Faker

from myapp.models import Product

''' Faker для отладки и дебаггинга '''
fake = Faker()
for i in range(1):
    name = fake.name()
    price = fake.random_int(1,10000)

    Product.objects.create(
        name=name,
        price=price
    )