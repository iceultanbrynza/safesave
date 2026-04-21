from django.db import models
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self._create_any_user(username, email, password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self._create_any_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def _create_any_user(self, username, email, password):
        if username is None:
            raise ValueError("Username is not given")

        if email is None:
            raise ValueError("Email is not given")

        if password is None:
            raise ValueError("Password is not given")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()