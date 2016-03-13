import json, os, sys
import requests

GHA_URL = 'https://api.github.com'
GHA_TOKEN = os.environ['GHA_TOKEN']
GHC_URL = 'https://githubcontributions.io/api'
USER = sys.argv[1]

def github(path):
    return requests.get(
        url='%s/%s' % (GHA_URL, path),
        headers={
            'Authorization': 'token %s' % GHA_TOKEN,
            'User-Agent': 'PSG',
        }
    )

repos = requests.get('%s/user/%s' % (GHC_URL, USER)).json()['repos']
frequencies = {}
for repo in repos:
    request = github('repos/%s/contributors' % repo)
    if request.status_code != 200:
        print('Bad repo: %s' % repo)
        continue
    contributors = request.json()
    for contributor in contributors:
        print(contributor['login'])
        login = contributor['login']
        if not login in frequencies:
            frequencies[login] = 1
        else:
            frequencies[login] += 1

with open('frequencies.json', 'w+') as f:
    f.write(json.dumps(frequencies, indent=2))
