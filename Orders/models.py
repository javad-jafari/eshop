from Products.models import ShopProduct
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', related_query_name='orders',
                             verbose_name=_(
                                 "user"), on_delete=models.CASCADE)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    discription = models.TextField(_('discription'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.user.mobile


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='paymentsorder', related_query_name='paymentsorder', verbose_name=_(
        "order"), on_delete=models.CASCADE)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='paymentsuser',
                                related_query_name='paymentsuser', verbose_name=_(
            "user"), on_delete=models.CASCADE)

    amount = models.IntegerField(_('amount'))

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return self.name


class Basket(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='baskets', related_query_name='baskets',
                                verbose_name=_(
                                    "user"), on_delete=models.CASCADE)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('update at'), auto_now=True)
    ordered = models.BooleanField(_('ordered'), default=False)

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Basketes')

    def __str__(self):
        return self.user.mobile

    def sum_total(self):
        sum = 0
        for item in self.itemsbasket.all():
            sum += item.price * item.quantity
        return sum


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, related_name='itemsbasket', related_query_name='itemsbasket', verbose_name=_(
        "basket"), on_delete=models.CASCADE)
    shop_product = models.ForeignKey(ShopProduct, related_name='itemsshop_product',
                                     related_query_name='itemsshop_product', verbose_name=_(
            "shop_product"), on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    price = models.PositiveIntegerField(_('price'), default=0)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('update at'), auto_now=True)

    class Meta:
        verbose_name = _('BasketDetail')
        verbose_name_plural = _('BasketDetails')

    def __str__(self):
        return self.basket.user.first_name

    def total_price(self):
        pric = self.price * self.quantity
        return pric




class OrderShopProduct(models.Model):
    order = models.ForeignKey(Order, related_name='Orderorder', related_query_name='Orderorder', verbose_name=_(
        "order"), on_delete=models.CASCADE)

    shop_product = models.ForeignKey(ShopProduct, related_name='Ordershop_product',
                                     related_query_name='Ordershop_product',
                                     verbose_name=_(
                                         "shop_product"), on_delete=models.CASCADE)
    count = models.IntegerField(_('count'))
