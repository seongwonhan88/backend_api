from django.db import models


class NormalUserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile_normal')
    timezone = models.CharField(max_length=100, null=True, blank=True)
