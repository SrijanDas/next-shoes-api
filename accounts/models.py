from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email=email, **extra_fields)
        user.set_password(password)
        user.is_admin = True
        user.is_active = True

        user.save()
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12)
    pincode = models.CharField(max_length=6)
    address = models.TextField()
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    land_mark = models.TextField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    verbose_name_plural = "Addresses"

    def __str__(self):
        return self.user.email




