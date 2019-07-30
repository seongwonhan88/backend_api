from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from members.apps import MembersConfig


class NormalUserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile_normal')
    timezone = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = MembersConfig.name + '_normal_user_profile'


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, **kwargs):
    if kwargs.get('created', False):
        NormalUserProfile.objects.create(user=instance)
        print('profile created')