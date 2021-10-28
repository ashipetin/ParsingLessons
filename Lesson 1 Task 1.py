import requests
username = 'ashipetin'
token = '###TOKEN###'
repos = requests.get('https://api.github.com/user/repos', auth=(username, token))
j_data = repos.json()
# pprint(j_data)
for repo in j_data:
    print(repo['name'])
