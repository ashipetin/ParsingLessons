import requests
username = 'ashipetin'
token = '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'
repos = requests.get('https://api.github.com/user/repos', auth=(username, token))
j_data = repos.json()
# pprint(j_data)
for repo in j_data:
    print(repo['name'])
