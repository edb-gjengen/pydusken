import json
import requests

class Members(object):
    __module__ = 'pydusken'

    def __init__(self, username, api_key, base_url):
        self._username = username
        self._api_key = api_key
        self._base_url = base_url

    def get(self, member_id, memberships=None, groups=None):
        resp = requests.get("{0}/member/{1}/".format(self._base_url, member_id), params=dict(username=self._username, api_key=self._api_key, memberships=memberships, groups=groups), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_groups(self, member_id):
        resp = requests.get("{0}/member/{1}/groups/".format(self._base_url, member_id), params=dict(username=self._username, key=self._api_key,), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def update(self, member_id, password=None):
        #TODO more attributes 
        resp = requests.patch("{0}/member/{1}/".format(self._base_url, member_id), params=dict(username=self._username, api_key=self._api_key), data=json.dumps(dict(password=password)), headers={'content-type': 'application/json'})
        resp.raise_for_status()
        # Response body is empty
        return True
