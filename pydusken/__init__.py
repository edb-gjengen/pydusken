import json
import requests
from urllib import quote_plus
from .members import Members
#from .membership import Memberships
#from .groups import Groups


class DuskenApi(object):
    def __init__(self, username, password, base_url="http://127.0.0.1:8000/api/v1"):
        self._base_url = base_url

        self._username = username
        self._api_key = self.get_api_key(username, password)
        self.members = Members(username, self._api_key, self._base_url)
        #self.memberships = Memberships(username, self._apikey, self._base_url)
        #self.groups = Groups(username, self._apikey, self._base_url)

    def set_creds(self, token):
        # TODO set creds for each type here 
        pass

    def get_api_key(self, username, password):
        resp = requests.post("http://127.0.0.1:8000/authenticate/".format(self._base_url), data=dict(username=username, password=password))
        resp.raise_for_status()
        return json.loads(resp.content).get('api_key')
