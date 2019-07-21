import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from members.apps import MembersConfig
from members.managers.custom_manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)

    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        db_table = MembersConfig.name + '_users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name}_{self.last_name}'


class TempUser(AbstractBaseUser):
    email = models.EmailField('email address', unique=True)
    is_active = models.BooleanField(default=False)
    date_activated = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)

    class Meta:
        db_table = MembersConfig.name + '_temp_user'