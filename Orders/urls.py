from django.urls import path, re_path
from .views import add_to_basket, basketlist, remove_item

urlpatterns = [

    # path('list/', BasketList.as_view(), name='basketlist'),
    path('list/', basketlist, name='basketlist'),
    path('list/additem/', add_to_basket, name='addbasketitem'),
    path('removeitem/<detail_id>', remove_item, name='removebasketitem'),
    
]
