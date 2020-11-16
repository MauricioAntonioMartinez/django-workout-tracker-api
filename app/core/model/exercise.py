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
# Maneger User class is the class that provides the creation
# of user or admin and all methods out of the box
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from user.custom_token import ExpiringToken

from app.settings import AUTH_USER_MODEL,BODY_PART_CHOICES,DIFFICULTY_CHOICES


class Exercise(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body_part = MultiSelectField(choices=BODY_PART_CHOICES,
                                 max_choices=3)
    # models.IntegerField(choices=BODY_PAT_CHOICES)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    notes = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BaseSerie(models.Model):
    reps = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)
    comment = models.TextField(blank=True)
    rpe = models.IntegerField(default=7,
                              validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        abstract = True


