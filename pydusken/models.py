from django.db import models
from django.contrib.auth.models import User

class DuskenAccessToken(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    scope = models.CharField(max_length=255)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u"{0} {1}".format(self.user, self.access_token)
