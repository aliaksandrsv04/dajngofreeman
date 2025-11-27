import time

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_page

from .forms import RegisterForm, ProductForm, OrderForm
from .models import Product, Category, Image, OrderItem, Order


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            login(request, user)  # сразу авторизуем пользователя
            return redirect('products')  # редирект на список товаров
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def products_view(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    products = Product.objects.prefetch_related('images').all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Order.objects.all().delete()
    # OrderItem.objects.all().delete()
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, 'products.html', {
        'products': page_obj,
        'categories': categories,
        'selected_category': category_id,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    products_images = product.images.all()
    return render(request, 'product_detail.html', {'product': product, 'products_images': products_images})


def add_to_cart(request, product_id):
    """Добавить товар в корзину (через сессию)."""
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    request.session['cart'] = cart
    return redirect('cart_view')

def remove_from_cart(request, product_id):
    """Удалить товар из корзины."""
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('cart_view')


def cart_view(request):
    """Показать корзину."""
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum(p.price for p in products)
    return render(request, 'cart.html', {'products': products, 'total': total})

def order_view(request):
    cart = request.session.get('cart', [])
    if cart == []:
        return redirect('products')
    products = Product.objects.filter(id__in=cart)
    total = sum(p.price for p in products)
    return render(request, 'order.html', {'products': products, 'total': total}, )

def order_new(request):
    cart = request.session.get('cart', [])
    if cart == []:
        return redirect('products')
    if request.user.is_authenticated:
        with transaction.atomic():
            order = Order()
            order.user = request.user
            order.telephone = request.user.phone
            order.email = request.user.email
            order.name = request.user.username
            order.save()
            messages.success(request, 'Заказ обработан успешно!')
            for product_id in request.session.get('cart', []):
                OrderItem.objects.create(order_id=order.id, product_id=product_id)
            request.session['cart'] = []
            return redirect('products')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.save()
                messages.success(request, 'Заказ обработан успешно!')
                for product_id in request.session.get('cart',[]):
                    OrderItem.objects.create(order_id=order.id, product_id =product_id)
                request.session['cart'] =  []

                return redirect('products')
    else:
        form = OrderForm()
    return render(request, 'order_new.html', {'form': form})
