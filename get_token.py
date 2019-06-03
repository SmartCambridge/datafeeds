#!/usr/bin/env python3

'''
Use a username and password found in environment variables
to request an API token and spit this out to stdout (from
where it can be put into uet another environment variable for
subsequent use)
'''

import os
import requests

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

get_token = 'https://api.vivacitylabs.com/get-token'


r = requests.post(
    get_token,
    data={'username': username, 'password': password},
    headers={'api-version': '2'}
)
r.raise_for_status()

all_data = r.json()
print(all_data['access_token'])
