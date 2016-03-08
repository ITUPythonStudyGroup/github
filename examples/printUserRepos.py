import requests
from myLib import *

"""
Fetches a list of organization repositories and prints their names.
"""

# Fetch a list of organization repositories
# https://developer.github.com/v3/repos/#list-organization-repositories
url = '%s/orgs/%s/repos' % (BASE, ORG)
response = requests.get(url)
repositories = response.json()

# Print the names of the repositories
for repository in repositories: print(repository['name'])
