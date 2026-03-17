from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def upload_avatar(instance, filename):
    return 'profile/profile_{id}/{filename}'.format(
        id=instance.user.id,
        filename=filename
    )



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=upload_avatar, null=True, blank=True)

