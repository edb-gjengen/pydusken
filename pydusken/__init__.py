import json
import requests
from urllib import quote_plus
from .members import Members
#from .membership import Memberships
#from .groups import Groups


class DuskenApi(object):
    def __init__(self, client_id, client_secret, base_url="http://127.0.0.1:8000/api/v1"):
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret

        #self.members = Members(username, self._api_key, self._base_url)
        #self.memberships = Memberships(username, self._apikey, self._base_url)
        #self.groups = Groups(username, self._apikey, self._base_url)

    def authenticate(self, username, password):
        return self.get_auth_token(username, password, scope='write')

    def get_auth_token(self, username, password, scope='read'):
        resp = requests.post(
            "{}/oauth2/access_token/".format(self._base_url),
            data=dict(
                username=username,
                password=password,
                client_id = self._client_id,
                client_secret = self._client_secret,
                scope=scope,
                grant_type='password'))

        resp.raise_for_status()

        return json.loads(resp.content)
