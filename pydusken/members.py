import json
import requests

class Members(object):
    __module__ = 'pydusken'

    def __request_auth_headers(self):
        return {
            'Authorization': "ApiKey {}:{}".format(self._username, self._api_key)
        }


    def __GET(self, url, headers={}, params={}):
        headers = dict(self.__request_auth_headers(), **headers)
        return requests.get(url, params=params, headers=headers)

    def __POST(self, url, params={}, headers={}, data=None):
        headers = dict(self.__request_auth_headers(), **headers)
        return requests.post(url, params=params, headers=headers, data=data)

    def __PATCH(self, url, params={}, headers={}, data=None):
        headers = dict(self.__request_auth_headers(), **headers)
        return requests.patch(url, params=params, headers=headers, data=data)

    def get_list(self, limit=None, offset=None):
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        resp = self.__GET("{0}/member/".format(self._base_url), params=params)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get(self, member_id, memberships=None, groups=None):
        resp = self.__GET("{0}/member/{1}/".format(self._base_url, member_id), params=dict(memberships=memberships, groups=groups))
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_groups(self, member_id):
        resp = self.__GET("{0}/member/{1}/groups/".format(self._base_url, member_id))
        resp.raise_for_status()
        return json.loads(resp.content)

    def update(self, member_id, password=None):
        #TODO more attributes 
        resp = self.__PATCH("{0}/member/{1}/".format(self._base_url, member_id), data=json.dumps(dict(password=password)), headers={'content-type': 'application/json'})
        resp.raise_for_status()
        # Response body is empty
        return True
