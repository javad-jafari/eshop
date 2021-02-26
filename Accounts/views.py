from django.contrib import messages
from django.contrib.auth import logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView, DetailView, UpdateView, FormView, CreateView, TemplateView

from Accounts.forms import UserThirdRegistrationForm, UserUpdateForm
from Accounts.models import Address, Shop
from Orders.models import BasketItem, Basket
from Products.models import Category, Product, ProductMeta, ShopProduct, Comment

User = get_user_model()


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = '/'


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'registration/register.html', {'form': UserThirdRegistrationForm})

    def post(self, request):
        form = UserThirdRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/accounts/login/')

        return render(request, 'registration/register.html', {'form': form})


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    login_url = '/'
    # redirect_field_name = 'home'
    template_name = 'registration/user_profile.html'
    pk_url_kwarg = 'user_id'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('user_id')
        try:
            context["address"] = Address.objects.filter(user__id=pk)
        except:
            context["address"] = None

        try:
            context["orderes"] = Basket.objects.filter(user_id=pk, ordered=True)
        except Basket.DoesNotExist:
            context["orderes"] = None
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', "last_name", 'mobile']
    template_name = 'registration/updateuser.html'
    pk_url_kwarg = 'user_id'


@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect(f'/accounts/userprofile/{user.id}')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/changepass.html', {
        'form': form
    })


class SellerProductView(LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'sale/seller_product.html'

    def get_success_url(self):
        return reverse('sellerprofile')


class SellerProductMetaView(LoginRequiredMixin, CreateView):
    model = ProductMeta
    fields = '__all__'
    template_name = 'sale/seller_productmeta.html'

    def get_success_url(self):
        return reverse('sellerprofile')


class SellerShopProductView(LoginRequiredMixin, CreateView):
    # model = ShopProduct
    fields = '__all__'
    template_name = 'sale/seller_shop_product.html'

    def get_queryset(self):
        return ShopProduct.objects.filter(shop__user_id=self.request.user.id)

    def get_success_url(self):
        return reverse('sellerprofile')


def sellerprofile(request):
    user = request.user.id
    context = {'shop_product': ShopProduct.objects.filter(shop__user_id=user),
               'comments': Comment.objects.filter()}
    return render(request, 'sale/seller_profile.html', context)
