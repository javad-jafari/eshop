from django.urls import path, include
from .views import CategoryDetailView, ProductDetailView, like_comment, create_comment, SearchResultsView, \
    SearchCatView, SearchBrandView

urlpatterns = [
    path('category/<slug:category_slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:product_slug>/<slug:shop_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('like_comment/', like_comment, name='like_comment'),
    path('comments/', create_comment, name='add_comment'),
    path('searchbar/', SearchResultsView.as_view(), name='searchbar'),
    path('searchcategory/', SearchCatView.as_view(), name='searchcategory'),
    path('searchbrand/', SearchBrandView.as_view(), name='searchbrand'),


]
