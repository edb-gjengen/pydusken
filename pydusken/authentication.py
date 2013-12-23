from django.conf import settings
from django.contrib.auth.models import User
from requests.exceptions import HTTPError

from . import *

from models import DuskenAccessToken

class DuskenBackend(object):

    def __init__(self):
        assert settings.DUSKEN_CLIENT_ID
        assert settings.DUSKEN_CLIENT_SECRET

        self._api = DuskenApi(client_id=settings.DUSKEN_CLIENT_ID, client_secret=settings.DUSKEN_CLIENT_SECRET)

    def authenticate(self, username=None, password=None):
        # Check the username/password and return a User.
        try:
            access_token = self._api.authenticate(username=username, password=password)
            try:
                user = User.objects.get(username=username)
                if not user.duskenaccesstoken:
                    d = DuskenAccessToken(access_token=access_token['access_token'], user=user)
                    d.save()
                else:
                    if user.duskenaccesstoken.access_token != access_token['access_token']:
                        user.duskenaccesstoken.access_token = access_token=access_token['access_token']
                        user.save()
            except User.DoesNotExist:
                # if user does not exist, create a local user
                user = User(username=username)
                user.set_unusable_password()
                user.save()
                DuskenAccessToken.objects.create(access_token=access_token['access_token'], user=user)

            return user

        except HTTPError as e:
            pass
        # TODO
        # if local user exist, sync email
        # return user with access_token
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
