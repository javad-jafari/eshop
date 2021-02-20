from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label=_('نام کاربری'), max_length=150, required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", }))

    password = forms.CharField(label=_('کلمه عبور'), widget=forms.PasswordInput(attrs={"class": "form-control"}),
                               required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        return password


class UserThirdRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='رمزعبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمزعبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'mobile')
        labels = {
            "email": _('ایمیل'),
            'mobile': _("موبایل")
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'passsword', 'email', 'avatar']
