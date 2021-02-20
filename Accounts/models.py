from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone


# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=90)
    last_name = models.CharField(_('last name'), max_length=90)
    passsword = models.CharField(_('password'), max_length=150)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    mobile = models.CharField(_('mobile'), max_length=12)
    avatar = models.ImageField(_('avatar'), upload_to='Accounts/User/image')
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return reverse('userprofile', kwargs={'user_id': self.id})


class UserEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(_('subject'), max_length=60)
    body = models.TextField(_('body'))

    class Meta:
        verbose_name = _('email')
        verbose_name_plural = _('emails')

    def __str__(self):
        return self.subject


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name=_('user'),related_name='user_address')
    city = models.CharField(_('city'), max_length=60)
    street = models.CharField(_('street'), max_length=160)
    alley = models.CharField(_('alley'), max_length=160)
    zip_code = models.CharField(_('zip_code'), max_length=160)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.city + self.street



class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=60)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.CharField(_('description'), max_length=260)
    image = models.ImageField(verbose_name=_('image'), upload_to='Accounts/Shop/image')

    class Meta:
        verbose_name = _('Shop')
        verbose_name_plural = _('Shopes')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'shop_slug': self.slug})
