from django.urls import path, re_path
from .views import add_to_basket, basketlist, remove_item, update_item, close_order, finished_order, add_address

urlpatterns = [


    path('list/', basketlist, name='basketlist'),
    path('list/additem/', add_to_basket, name='addbasketitem'),
    path('removeitem/<detail_id>', remove_item, name='removebasketitem'),
    path('updateitem/', update_item, name='updatebasketitem'),
    path('checkout/', close_order, name='checkout'),
    path('addadress/', add_address, name='add_address'),

    path('checkout/order', finished_order, name='finished_order'),

]
