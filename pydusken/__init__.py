import logging
import json
import requests
from urllib import quote_plus
from .members import Members
#from .membership import Memberships
#from .groups import Groups

class DuskenBaseModel:
    pass


class DuskenApi(object):
    def __init__(self, client_id, client_secret, base_url="http://127.0.0.1:8000/api/v1"):
        self.base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret

        self.members = Members(self)
        #self.memberships = Memberships(username, self._apikey, self._base_url)
        #self.groups = Groups(username, self._apikey, self._base_url)

    def set_access_token(self, access_token):
        self.access_token = access_token

    def is_authenticated(self):
        return hasattr(self, 'access_token') and self.access_token

    def authenticate(self, username, password):
        try:
            self.oauth2_access_token = self.get_access_token(username, password, scope='read+write')
            self.access_token = self.oauth2_access_token['access_token']
        except requests.exceptions.HTTPError as e:
            logging.error("Could not authenticate with API. Correct client_id, client_secret, username and password?\n{0}".format(e))
            return None

        return self.oauth2_access_token

    def get_access_token(self, username, password, scope='read'):
        resp = requests.post(
            "{0}/oauth2/access_token/".format(self.base_url),
            data=dict(
                username=username,
                password=password,
                client_id = self._client_id,
                client_secret = self._client_secret,
                scope=scope,
                grant_type='password'))

        resp.raise_for_status()

        return json.loads(resp.content)

    def raise_for_status(self, resp):
        """
            Custom raise_for_status that raises stored :class:`HTTPError` on resp, if one occurred.
            Prints Error message from Dusken API
        """

        http_error_msg = ''

        if 400 <= resp.status_code < 500:
            http_error_msg = '%s Client Error: %s %s' % (resp.status_code, resp.reason, resp.content)

        elif 500 <= resp.status_code < 600:
            http_error_msg = '%s Server Error: %s %s' % (resp.status_code, resp.reason, resp.content)

        if http_error_msg:
            raise requests.exceptions.HTTPError(http_error_msg, response=resp)

