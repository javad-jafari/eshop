from django import forms


class BasketDetailForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    shop_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.NumberInput(), initial=1)
