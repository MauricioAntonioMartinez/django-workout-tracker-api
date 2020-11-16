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

from .exercise import BaseSerie



class Serie(BaseSerie):
    father_set = models.ForeignKey(
        'Set', on_delete=models.CASCADE, related_name='series')


class Set(models.Model):
    exercise = models.ForeignKey(
        'Exercise', on_delete=models.CASCADE,)
    work_out = models.ForeignKey(
        'WorkOut', on_delete=models.CASCADE)


class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    workout_date = models.DateField()
    sets = models.ManyToManyField('Exercise', through=Set, blank=True)

    class Meta:
        ordering = ['workout_date']