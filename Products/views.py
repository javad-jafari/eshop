from itertools import product

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView

from Orders.forms import BasketDetailForm
from Products.forms import CommentForm
from Products.models import Product, ShopProduct, Comment, like, ProductMeta
from Products.models import Category
import json
from django.db import transaction


# Create your views here.


class ProductDetailView(DetailView):
    model = ShopProduct
    template_name = 'product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_object(self):
        slug1 = self.kwargs.get('product_slug')
        slug2 = self.kwargs.get('shop_slug')
        item = get_object_or_404(ShopProduct, product__slug=slug1, shop__slug=slug2)
        item.incrementViewCount()
        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug1 = self.kwargs.get('product_slug')
        slug2 = self.kwargs.get('shop_slug')
        context["comments"] = Comment.objects.filter()
        context["metas"] = ProductMeta.objects.filter(product__slug=self.kwargs.get('product_slug'))
        item = get_object_or_404(ShopProduct, product__slug=slug1, shop__slug=slug2)
        context['form'] = CommentForm()
        context['basketform'] = BasketDetailForm(initial={'product_id': item.product_id, 'shop_id': item.shop_id})
        return context


class CategoryDetailView(ListView):
    model = ShopProduct
    template_name = 'category.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category.objects.filter(), slug=slug)
        context["shopproducts"] = ShopProduct.objects.filter(
            Q(product__category=category) | Q(product__category__parent=category))

        return context


@csrf_exempt
def like_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.get(id=data['comment_id'])
    except Comment.DoesNotExist:
        return HttpResponse('bad request', status=404)
    try:
        comment_like = like.objects.get(user=user, comment=comment)
        comment_like.condition = data['condition']
        comment_like.save()
    except like.DoesNotExist:
        like.objects.create(user=user, condition=data['condition'], comment=comment)
    result = {'like_count': comment.like_count, 'dislike_count': comment.dislike_count}

    return HttpResponse(json.dumps(result), status=201)


@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.create(product_id=data['product_id'], content=data['content'], author=user)
        result = {"comment_id": comment.id, "content": comment.content, 'dislike_count': 0, 'like_count': 0,
                  'full_name': user.email}
        return HttpResponse(json.dumps(result), status=201)
    except:
        result = {"error": 'error'}
        return HttpResponse(json.dumps(result), status=400)


class SearchResultsView(ListView):
    model = ShopProduct
    template_name = 'search/searchbar.html'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = ShopProduct.objects.filter(
            Q(product__name__contains=query) | Q(product__slug__contains=query) | Q(
                product__category__name__contains=query)
        )
        return object_list


class SearchCatView(ListView):
    model = ShopProduct
    template_name = 'search/categorysearch.html'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('categorysearch')
        object_list = ShopProduct.objects.filter(Q(product__category__name__contains=query))
        return object_list


class SearchBrandView(ListView):
    model = ShopProduct
    template_name = 'search/brandsearch.html'
    paginate_by = 6

    def get_queryset(self):
        val = ""
        for key, value in self.request.GET.items():
            print("%s %s" % (key, value))
            val += value

        object_list = ShopProduct.objects.filter(Q(product__brand__name__icontains=val))

        return object_list


class Sorted(ListView):
    model = ShopProduct
    template_name = 'search/categorysearch.html'
    paginate_by = 6

    def get_queryset(self):
        for key, value in self.request.GET.items():
            print(type(value))
            if value == '1':
                object_list = ShopProduct.objects.filter(product__brand__name='گوچی').order_by('product__seen')
                return object_list

            elif value == '2':
                object_list = ShopProduct.objects.filter(product__brand__name='گوچی').order_by('-price')
                return object_list
            elif value == '3':
                object_list = ShopProduct.objects.filter(product__brand__name='گوچی').order_by('price')
                return object_list
