import requests
from pprint import pprint
url = 'https://api.vk.com/method/groups.get'
access_token = '###TOKEN###'
v = '5.81'
user_id = '5977095'
response = requests.get(url, params={
    'user_id':user_id,
    'access_token':access_token,
    'v':v})
result = response.json()
pprint(result)