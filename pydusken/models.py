from django.db import models
from django.contrib.auth.models import User

class DuskenAccessToken(models.Model):
    access_token = models.CharField(max_length=255)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u"{} {}".format(self.user, self.access_token)
