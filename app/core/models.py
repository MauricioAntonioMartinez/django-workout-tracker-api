import os
import uuid

from django.conf import settings  # this is how we can retrive variables
# for the settings file
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Maneger User class is the class that provides the creation
# of user or admin and all methods out of the box


def recipe_image_file_path(instance, file_name):
    """Generate file path for new recipe image

    Args:
        instance : instance of the current session
        file_name (str): file name with the extension
    """
    ext = file_name.split('.')[-1]  # the last item
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe/', filename)


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


class Exercise(models.Model):
    DIFFICULTY_CHOICES = (
        (1, 'EASY'),
        (2, 'NORMAL'),
        (3, 'HARD'),
        (4, 'PRO'),
    )

    BODY_PAT_CHOICES = (
        (1, 'CHEST'),
        (2, 'BICEP'),
        (3, 'CALFS'),
        (4, 'HASTRINGS'),
        (5, 'QUADRICEPS'),
        (6, 'TRICEPS'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body_part = models.IntegerField(choices=BODY_PAT_CHOICES)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    notes = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    exercise = models.CharField(max_length=1, blank=True)


class BaseSerie(models.Model):
    reps = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)
    comment = models.TextField(blank=True)
    rpe = models.IntegerField(default=7,
                              validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        abstract = True


class Serie(BaseSerie):
    father_set = models.ForeignKey(
        'Set', on_delete=models.CASCADE, related_name='series')


class SerieRoutine(BaseSerie):
    father_set = models.ForeignKey(
        'SetRoutine', on_delete=models.CASCADE, related_name='series')


class Set(models.Model):
    exercise = models.ForeignKey(
        'Exercise', on_delete=models.CASCADE,)
    work_out = models.ForeignKey(
        'WorkOut', on_delete=models.CASCADE)


class SetRoutine(models.Model):
    exercise = models.ForeignKey(
        'Exercise', on_delete=models.CASCADE)
    routine = models.ForeignKey(
        'RoutineDay', on_delete=models.CASCADE)


class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    workout_date = models.DateField()
    sets = models.ManyToManyField('Exercise', through=Set, blank=True)

    class Meta:
        ordering = ['workout_date']


class RoutineDay(models.Model):
    name = models.CharField(max_length=255, blank=True)
    routine = models.ForeignKey(
        'Routine', related_name='routines', on_delete=models.CASCADE)

    def sets(self):
        return SetRoutine.objects.filter(routine=self)


class Routine(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
