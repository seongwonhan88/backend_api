import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from members.apps import MembersConfig
from members.managers.custom_manager import CustomUserManager


class User(AbstractUser):
    uuid = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = email
    objects = CustomUserManager()

    class Meta:
        db_table = MembersConfig.name + '_users'
