import os
import uuid

from django.conf import settings  # this is how we can retrive variables
# for the settings file
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from user.custom_token import ExpiringToken
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication




class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kargs):
        """Creates and saves a new user
        Args:
            email ([type]): [description]
            password ([type], optional): [description]. Defaults to None.
        """
        if not email:
            raise ValueError('User Must Have An Email Address')
        new_email = self.normalize_email(email)
        user = self.model(email=new_email, **kargs)
        # this is the same as creating a user model
        user.set_password(password)  # this incrypt the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        # create a normal user
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True  # adding the fields of a superuser
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):  # this classes provides
    # all the free functionality out of the box that django provides
    # with this we can customize
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class ExpiringTokenAuthentication(TokenAuthentication):
    """Overwrites the normal rest framework auth token model"""
    model = ExpiringToken

    def authenticate_credentials(self, key):
        """Middleware in charge to validate the given token"""
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        if token.expired():
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)

