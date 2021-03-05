from django import forms

from Accounts.models import Address


class BasketDetailForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    shop_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.NumberInput(), initial=1)


class OrderedForm(forms.Form):
    Basket_id = forms.IntegerField(widget=forms.HiddenInput())


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
