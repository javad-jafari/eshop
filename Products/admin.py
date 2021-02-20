from django.contrib import admin

from .models import Product, ShopProduct, Category, Comment, Brand, ProductMeta, like


# Register your models here.


class ChildrenItemInline(admin.TabularInline):
    model = Category
    fields = (
        'name', 'slug'
    )
    extra = 1
    show_change_link = True


class ProductItemInline(admin.TabularInline):
    model = ProductMeta
    fields = (
        'value', 'product', 'label'
    )
    extra = 1
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'parent')
    search_fields = ('slug', 'name')
    list_filter = ('parent',)
    inlines = [
        ChildrenItemInline,
    ]


@admin.register(ShopProduct)
class ShopProduct(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'quantity')
    search_fields = ('shop', 'product')
    list_filter = ('shop',)



@admin.register(Brand)
class Brand(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'seen',)
    search_fields = ('name',)
    list_filter = ('brand', 'category', 'name')
    inlines = [
        ProductItemInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_confirmed', 'author', 'like_count', 'dislike_count')
    search_fields = ('content',)
    list_filter = ('is_confirmed',)
    date_hierarchy = 'create_at'


@admin.register(like)
class likeAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(ProductMeta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ('label','value','product')