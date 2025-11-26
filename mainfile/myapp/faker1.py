import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from faker import Faker

from .models import Product

fake = Faker()
for i in range(20):
    name = fake.name()
    price = fake.random_int(1,10000)

    Product.objects.create(
        name=name,
        price=price
    )