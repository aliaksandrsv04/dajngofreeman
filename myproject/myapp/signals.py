import re

import telebot
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, OrderItem, Product

bot = telebot.TeleBot('7988808659:AAGcAN9OuQF0AspY5-HyU81wgSfHioEnlAo')

def send_order_notification(instance):
    mess = ''
    order_item = OrderItem.objects.filter(order_id=instance.id)
    for item in order_item:
        mess += item.product.name + ', '
    a = f'Продукты: {mess} телефон: {instance.telephone}, имя: {instance.name}, email: {instance.email}, ID заказа: {instance.id}'
    bot.send_message(1199675138, a
                     )
    return a
@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    str1 = ''
    if created:
        transaction.on_commit(lambda: send_order_notification(instance))


    else:
        print(instance.name)

