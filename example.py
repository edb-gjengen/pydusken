import pprint
import json

import pydusken

# credentials
username = "admin"
password = "admin"

# setup client
client = pydusken.DuskenApi(username=username, password=password)

# get member
pprint.pprint(client.members.get('1'))

# get member groups
pprint.pprint(client.members.get_groups('1'))

# update member password to the same password as you have
pprint.pprint(client.members.update('1', password='admin'))
