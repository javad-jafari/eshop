import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView

from Accounts.models import Address
from Orders.models import BasketItem, Basket
from Products.models import Category, ShopProduct
from Orders.forms import BasketDetailForm, OrderedForm, AddAddressForm


@login_required(login_url='/accounts/login')
def basketlist(request):
    context = {'basket': None, 'detail': None}

    open_basket: Basket = Basket.objects.filter(user_id=request.user.id, ordered=False).first()
    if open_basket is not None:
        context['basket'] = open_basket
        context['detail'] = open_basket.itemsbasket.all()
        context['total_price'] = open_basket.sum_total()
        context['order_form'] = OrderedForm(initial={'Basket_id': open_basket.id})
        context['address'] = Address.objects.filter(user_id=request.user.id)
        context['AddressForm'] = AddAddressForm()

    return render(request, 'order/basketlist.html', context)


@login_required(login_url='/accounts/login')
def add_to_basket(request):
    new_basket_form = BasketDetailForm(request.POST or None)
    if new_basket_form.is_valid():
        basket = Basket.objects.filter(user_id=request.user.id, ordered=False).first()

        if basket is None:
            basket = Basket.objects.create(user_id=request.user.id, ordered=False)

        product_id = new_basket_form.cleaned_data.get('product_id')
        shop_id = new_basket_form.cleaned_data.get('shop_id')
        quantity = new_basket_form.cleaned_data.get('quantity')
        if quantity < 0:
            quantity = 1
        shop_product = ShopProduct.objects.get(product_id=product_id, shop_id=shop_id)
        if basket.itemsbasket.filter(shop_product_id=shop_product.id).exists():
            pass
        else:
            basket.itemsbasket.create(shop_product_id=shop_product.id, price=shop_product.price, quantity=quantity)
        return redirect('basketlist')

    return redirect('/')


@login_required(login_url='/accounts/login')
def remove_item(request, *args, **kwargs):
    detail_id = kwargs.get('detail_id')

    if detail_id is not None:
        basket_item = BasketItem.objects.get_queryset().get(id=detail_id, basket__user_id=request.user.id)
        if basket_item is not None:
            basket_item.delete()
            return redirect('/basket/list')
    raise Http404()


@csrf_exempt
def update_item(request):
    data = json.loads(request.body)
    user = request.user.id
    basket = BasketItem.objects.get(id=data['item_id'], basket__user_id=user)
    basket.quantity += data['condition']
    basket.save()
    if basket.quantity < 1:
        basket.delete()

    response = {"counters": basket.quantity, 'price_item': basket.total_price(),
                'price_total': basket.basket.sum_total()}

    return HttpResponse(json.dumps(response), status=201)


@login_required(login_url='/accounts/login')
def close_order(request):
    forms = OrderedForm(request.POST or None)
    if forms.is_valid():
        bask_id = forms.cleaned_data.get('Basket_id')
        basket = Basket.objects.get(user_id=request.user.id, id=bask_id, ordered=False)
        basket.ordered = True
        basket.save()

        return redirect('checkout')
    return redirect('finished_order')


@login_required(login_url='/accounts/login')
def finished_order(request):
    context = {'basket': None, 'detail': None}
    finish: Basket = Basket.objects.filter(user_id=request.user.id, ordered=True).first()
    if finish is not None:
        context['basket'] = finish
        context['detail'] = finish.itemsbasket.all()
        context['address'] = Address.objects.filter(user_id=request.user.id).first()
        context['total_price'] = finish.sum_total()

    return render(request, 'order/checkout.html', context)


@login_required(login_url='/accounts/login')
def add_address(request):
    forms = AddAddressForm(request.POST or None)
    if forms.is_valid():
        city = forms.cleaned_data.get('city')
        street = forms.cleaned_data.get('street')
        alley = forms.cleaned_data.get('alley')
        zip_code = forms.cleaned_data.get('zip_code')
        new_address = Address.objects.create(user_id=request.user.id, city=city, street=street,
                                          alley=alley, zip_code=zip_code)

        new_address.save()

        return redirect('basketlist')
    return redirect('basketlist')
