from django.contrib import admin

from .models import Product, Category, Image, Order


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('in_stock', 'category')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'product')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'telephone', 'email')