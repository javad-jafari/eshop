from django.urls import path, re_path
from .views import (LogoutView,
                    RegisterView,
                    SignView,
                    UserProfileView,
                    ProfileUpdate,
                    change_password,
                    SellerProductView,SellerProductMetaView,SellerShopProductView,sellerprofile)

urlpatterns = [

    path('login/', SignView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('userprofile/<int:user_id>/', UserProfileView.as_view(), name='userprofile'),
    path('userprofileupdate/<int:user_id>/', ProfileUpdate.as_view(), name='userprofileupdate'),
    path('password/', change_password, name='change_password'),
    path('seller/products/<int:user_id>/', SellerProductView.as_view(), name='sellerproduct'),
    path('seller/productmetas/<int:user_id>/', SellerProductMetaView.as_view(), name='sellerproductmetas'),
    path('seller/shop-product/<int:user_id>/', SellerShopProductView.as_view(), name='sellershopproduct'),
    path('sellerprofile/', sellerprofile, name='sellerprofile'),

]
