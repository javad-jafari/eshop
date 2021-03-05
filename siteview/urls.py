from django.urls import path, include
from .views import HomeView, AboutView, ServiceView, ShopesView,ShopeDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about-us', AboutView.as_view(), name='about'),
    path('service', ServiceView.as_view(), name='service'),
    path('shopes', ShopesView.as_view(), name='shopes'),
    path('shopes/<slug:shope_slug>/', ShopeDetailView.as_view(), name='shop_detail'),
]
