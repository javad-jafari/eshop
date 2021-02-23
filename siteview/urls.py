from django.urls import path, include
from .views import HomeView,AboutView,ServiceView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about-us', AboutView.as_view(), name='about'),
    path('service', ServiceView.as_view(), name='service'),
]
