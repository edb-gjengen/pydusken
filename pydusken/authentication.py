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

        TODO: permission methods: get_group_permissions(), get_all_permissions(), has_perm(), and has_module_perms()
    """

    def __init__(self):
        assert settings.DUSKEN_CLIENT_ID
        assert settings.DUSKEN_CLIENT_SECRET

        if hasattr(settings,'DUSKEN_BASE_URL'):
            self._api = DuskenApi(client_id=settings.DUSKEN_CLIENT_ID, client_secret=settings.DUSKEN_CLIENT_SECRET, base_url=settings.DUSKEN_BASE_URL)
        else:
            self._api = DuskenApi(client_id=settings.DUSKEN_CLIENT_ID, client_secret=settings.DUSKEN_CLIENT_SECRET)

    def _is_using_email(self, username):
        try:
            validate_email(username)
            return True
        except ValidationError as e:
            return False

    def _get_or_create_local_user(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # if user does not exist, create a local user
            user = User(username=username)
            user.set_unusable_password()
            user.save()

        return user

    def _refresh_access_token(self, user, access_token):
        d = DuskenAccessToken.objects.filter(user=user)
        if len(d) == 0:
            d = DuskenAccessToken(user=user)
        else:
            d = d[0]

        d.access_token = access_token['access_token']
        d.expires_in = access_token['expires_in']
        d.refresh_token = access_token['refresh_token']
        d.scope = access_token['scope']
        d.save()

    def _sync_user_detail(self, user):
        me = self._api.members.me()['objects'][0]
        attrs = ['email', 'first_name', 'last_name']
        [setattr(user, attr, me[attr]) for attr in attrs]
        user.save()

    def authenticate(self, username=None, password=None):
        # TODO Username can be an email
        #is_using_email = self._is_using_email(username)
        #access_token = self._api.authenticate(email=username, password=password)
        try:
            access_token = self._api.authenticate(username, password)
        except HTTPError as e:
            # Did not authenticate
            return None
            
        if not access_token:
            return None

        user = self._get_or_create_local_user(username)
        self._refresh_access_token(user, access_token)
        self._sync_user_detail(user)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
