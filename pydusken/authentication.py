from django.conf import settings
from django.contrib.auth.models import User
from requests.exceptions import HTTPError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from . import *

from models import DuskenAccessToken

class DuskenBackend(object):
    """
        Django Authentication Backend
    """

    def __init__(self):
        assert settings.DUSKEN_CLIENT_ID
        assert settings.DUSKEN_CLIENT_SECRET

        self._api = DuskenApi(client_id=settings.DUSKEN_CLIENT_ID, client_secret=settings.DUSKEN_CLIENT_SECRET)

    def _is_using_email(self, username):
        try:
            validate_email(username)
            return True
        except ValidationError as e:
            return False

    def _sync_user_detail(self, user):
        me = self._api.members.me()['objects'][0]
        attrs = ['email', 'first_name', 'last_name']
        [setattr(user, attr, me[attr]) for attr in attrs]
        user.save()

    def authenticate(self, username=None, password=None):
        # Check the username/password and return a User. Username can be an email
        is_using_email = self._is_using_email(username)
        try:
            if is_using_email:
                access_token = self._api.authenticate(email=username, password=password)
            else:
                access_token = self._api.authenticate(username=username, password=password)

            if not access_token:
                return None

            try:
                if is_using_email:
                    user = User.objects.get(email=username)
                else:
                    user = User.objects.get(username=username)
                if not user.duskenaccesstoken:
                    d = DuskenAccessToken(access_token=access_token, user=user)
                    d.save()
                else:
                    # refresh access_token
                    if user.duskenaccesstoken.access_token != access_token:
                        user.duskenaccesstoken.access_token = access_token=access_token
                        user.save()
            except User.DoesNotExist:
                # if user does not exist, create a local user
                user = User(username=username)
                user.set_unusable_password()
                user.save()
                DuskenAccessToken.objects.create(access_token=access_token['access_token'], user=user)

            self._sync_user_detail(user)

            return user

        except HTTPError as e:
            # Did not authenticate
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
