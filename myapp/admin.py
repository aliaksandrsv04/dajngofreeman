from django.contrib import admin
import csv
from .models import Product, Category, Image, Order, CustomUser



''' 
Фича с выгрузкой информации в CSV файл 

Ловим кверисет достаем ключи, испльзуем их как названия, и словарями из квери сета заполняем инфо 
'''
@admin.action(description="To CSV")
def make_published(modeladmin, request, queryset):
    qs = queryset.values()
    print(qs)
    mylist = qs[0].keys()
    print(mylist)
    with open('info.csv', 'w', newline='') as csvfile:
        fieldnames = mylist
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in qs:
            writer.writerow(i)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('in_stock', 'category')
    #выгрузка для класса Продукты
    actions = [make_published]


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = ('username',)
    exclude = ('password',)

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