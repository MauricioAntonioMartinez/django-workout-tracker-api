from django.conf import settings  # this is how we can retrive variables
# for the settings file
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

# Maneger User class is the class that provides the creation
# of user or admin and all methods out of the box


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


class Tag(models.Model):
    """Tag to be used for a recipie
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name
