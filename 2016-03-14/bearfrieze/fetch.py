import json, os, sys
import requests

GHA_URL = 'https://api.github.com'
GHA_TOKEN = os.environ['GHA_TOKEN']
USER = sys.argv[1]
LIMIT = 10

def edge_key(a, b):
    return ':'.join(sorted([a, b]))

def github(path):
    return requests.get(
        url='%s/%s' % (GHA_URL, path),
        headers={
            'Authorization': 'token %s' % GHA_TOKEN,
            'User-Agent': 'PSG',
        }
    )

def user_frequencies(user):
    print('Getting frequencies for %s' % user)
    repos = github('users/%s/repos?type=all&sort=pushed' % user).json()
    frequencies = {}
    for repo in repos[:LIMIT]:
        request = github('repos/%s/contributors' % repo['full_name'])
        if request.status_code != 200:
            print('Bad repo: %s' % repo['name'])
            continue
        contributors = request.json()
        for contributor in contributors:
            print(contributor['login'])
            login = contributor['login']
            if not login in frequencies:
                frequencies[login] = 1
            else:
                frequencies[login] += 1
    if user in frequencies: del frequencies[user]
    return frequencies

frequencies = {}
fs = user_frequencies(USER)
frequencies[USER] = fs
logins_sorted = [t[0] for t in sorted(fs.items(), key=lambda t: t[1], reverse=True)]
for login in logins_sorted[:min(LIMIT, len(logins_sorted))]:
    frequencies[login] = user_frequencies(login)

edges = {}
for a in frequencies.keys():
    for b in frequencies[a]:
        key = edge_key(a, b)
        if not key in edges: edges[key] = 0
        edges[key] += frequencies[a][b]

with open('%s-frequencies.json' % USER, 'w+') as f:
    f.write(json.dumps(frequencies, indent=2))

with open('%s-edges.json' % USER, 'w+') as f:
    f.write(json.dumps(edges, indent=2))
