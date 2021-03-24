from django.contrib import admin
from django.db import models
from .models import Basket, BasketItem, Order, Payment, OrderShopProduct


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'create_at')
    search_fields = ('create_at',)
    list_filter = ('user',)
    date_hierarchy = 'create_at'
    empty_value_display = '-empty-'


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
    list_filter = ('user',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount')
    search_fields = ('order',)
    list_filter = ('order',)


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'shop_product', 'quantity', 'price', 'size', 'color')
    search_fields = ('basket',)
    list_filter = ('basket',)


@admin.register(OrderShopProduct)
class OrderShopProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'shop_product', 'count')
    search_fields = ('order',)
    list_filter = ('order',)
