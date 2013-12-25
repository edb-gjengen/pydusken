import pprint
import json

import pydusken

# oauth
client_id = "d802768a8afd9dec2660"
client_secret = "3962467fe60a94727812053c8a4f44533f4ef610"

# credentials
username = "admin"
password = "admin"

# setup client
client = pydusken.DuskenApi(client_id, client_secret)

client.authenticate(username, password)

# get member
pprint.pprint(client.members.get('1'))

# get member groups
pprint.pprint(client.members.get_groups('1'))

# update member password to the same password as you have
pprint.pprint(client.members.update('1', address='admin'))

# filter members
pprint.pprint(client.members.filter(email="nikolai@studentersamfundet.no"))
