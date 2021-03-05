from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from Accounts.models import Shop
from .models import SlideShow
from Products.models import Category, Product, ShopProduct, Comment


# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slides"] = SlideShow.objects.all()
        context["product"] = ShopProduct.objects.all()[:8]
        return context


class AboutView(TemplateView):
    template_name = 'aboutus.html'


class ServiceView(TemplateView):
    template_name = 'service.html'


class ShopesView(TemplateView):
    template_name = 'shops.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shopes'] = Shop.objects.all()
        return context


class ShopeDetailView(TemplateView):
    template_name = 'shope_detail.html'
    slug_url_kwarg = 'shope_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('shope_slug')
        context['pros'] = ShopProduct.objects.filter(shop__slug=slug)
        context['shope'] = Shop.objects.get(slug=slug)
        context['comments'] = Comment.objects.filter(product__ShopProducts__shop__slug =slug)
        return context
