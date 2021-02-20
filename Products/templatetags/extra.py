from django import template

from Products.models import ShopProduct

register = template.Library()


@register.filter(name='dictkey')
def dictkey(lst):
    for key in lst:
        return lst[key]
