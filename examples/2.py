import requests, re

BASE = 'https://api.github.com'
ORG = 'ITUPythonStudyGroup'

def strip_url_parameters(url): return re.sub(r'\{.*\}', '', url)

# Feth a list of organization repositories
# https://developer.github.com/v3/repos/#list-organization-repositories
url = '%s/orgs/%s/repos' % (BASE, ORG)
repositories = requests.get(url).json()

# Print the commit messages of all commits for each repository
for repository in repositories:
    url = strip_url_parameters(repository['commits_url'])
    commits = requests.get(url).json()
    print('%s:' % repository['name'])
    for commit in commits: print('- %s' % commit['commit']['message'])
    print()
