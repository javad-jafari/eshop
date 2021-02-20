from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm

from .models import Address, Shop, User, UserEmail
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'is_staff','mobile']
    change_password_form = AdminPasswordChangeForm
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (_('authentication data'), {
            "fields": (
                'email',
                'password',
            ),
        }),
        (_('Personal info'), {
            "fields": ('first_name','last_name', 'avatar')
        }),
        (_('Permissions'), {
            "fields": ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            "fields": ('last_login',)
        }),
    )

@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ('user','subject')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','city','street')

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('user','name','slug')


