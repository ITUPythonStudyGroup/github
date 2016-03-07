import requests, re
from multiprocessing import Pool

BASE = 'https://api.github.com'
ORG = 'ITUPythonStudyGroup'

def strip_url_parameters(url): return re.sub(r'\{.*\}', '', url)

def get_commits(repository):
    url = strip_url_parameters(repository['commits_url'])
    return requests.get(url).json()

# Feth a list of organization repositories
# https://developer.github.com/v3/repos/#list-organization-repositories
url = '%s/orgs/%s/repos' % (BASE, ORG)
repositories = requests.get(url).json()

# Retrieve commits for each repository in parallel and print the commit messages
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.map
# https://developer.github.com/v3/repos/commits/#list-commits-on-a-repository
with Pool(len(repositories)) as pool:
    commits = pool.map(get_commits, repositories)
    for repository, commits in zip(repositories, commits):
        print('%s:' % repository['name'])
        for commit in commits: print('- %s' % commit['commit']['message'])
        print()
