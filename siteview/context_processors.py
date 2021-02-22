from django.utils import timezone

from Orders.models import Basket, BasketItem
from Products.models import Category


def headers(request):
    return {
        'categories': Category.objects.all(),
        'bas_d': BasketItem.objects.filter(basket__user_id=request.user.id, basket__ordered=False),
        "time": timezone.now()
    }
