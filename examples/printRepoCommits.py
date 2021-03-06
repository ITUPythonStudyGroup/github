import requests, re
from myLib import *

"""
Fetches a list of organization repositories and prints the commit messages of all the commits for each repository.
"""

# Fetch a list of organization repositories
# https://developer.github.com/v3/repos/#list-organization-repositories
url = '%s/orgs/%s/repos' % (BASE, ORG)
repositories = requests.get(url).json()

# Print the commit messages of all commits for each repository
# https://developer.github.com/v3/repos/commits/#list-commits-on-a-repository
for repository in repositories:
    url = strip_url_parameters(repository['commits_url'])
    commits = requests.get(url).json()
    print('%s:' % repository['name'])
    for commit in commits: print('- %s' % commit['commit']['message'])
    print()
