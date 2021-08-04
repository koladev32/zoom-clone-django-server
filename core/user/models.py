from django.db import models
from django.contrib.auth.models import (BaseUserManager, PermissionsMixin, AbstractBaseUser)
from core.abstract.models import AbstractModel, AbstractManager


class UserManager(BaseUserManager, AbstractManager):

    def create_user(self, username, password):

        if username is None:
            raise TypeError("You should provide an username.")

        if password is None:
            raise TypeError("You should put a password")

        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractModel, PermissionsMixin, AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username
