from django.db import models

from members.apps import MembersConfig


class NormalUserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile_normal')
    timezone = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = MembersConfig.name + '_normal_user_profile'
