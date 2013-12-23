from django.db import models
from django.contrib.auth.models import User

class DuskenAccessToken(models.Model):
    access_token = models.CharField(max_length=255)
    user = models.OneToOneField(User)
