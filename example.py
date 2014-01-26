import pprint
import json

import pydusken

# oauth
client_id = "4c90c83fa400acadafdf"
client_secret = "49d2c94c50da6216059f44d89bd87fa18b31f9f7"

# credentials
username = "admin"
password = "admin"

# setup client
client = pydusken.DuskenApi(client_id, client_secret)

client.authenticate(username, password)

# get member
pprint.pprint(client.members.get('1'))

# get authenticated user 
pprint.pprint(client.members.me())

# get member groups
pprint.pprint(client.members.get_groups('1'))

# update member password to the same password as you have
pprint.pprint(client.members.update('1', password='admin'))

# filter members
pprint.pprint(client.members.filter(email="nikolai@studentersamfundet.no"))
