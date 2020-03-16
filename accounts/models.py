from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .managers import CustomUserManager

class MyUser(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    username 		= models.CharField(max_length=30, unique=True)
    fullname        = models.CharField(verbose_name='full name', max_length=50, blank=True)

    is_active       = models.BooleanField(default=False)
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    #is_staff = models.BooleanField(default=False) can be removed if not using Django Admin
    #is_admin can be removed if not using Django Admin

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'username',]

    #email & password is auto required , no need to implement in REQUIRED_FIELD 

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
