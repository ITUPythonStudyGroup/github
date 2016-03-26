'''
Limitation of the Search API:
1. "This method returns up to 100 results per page."  
2. "Only the first 1000 search results are available."
Possible solution: Get the data by pages with 100 results. Join the data later. 
Chunk up / specify the search querries to stay under the 1000 limit. 
For more information, see: https://developer.github.com/v3/search/#rate-limit
'''

## Import libraries
import urllib.request as ur
import requests
import json
import collections

#########################################
### Accessing data via the GitHub API ###
#########################################

'''
Please fill out the TOKEN and the TERM and LNG sections.
'''

TOKEN = 'Add your token here'
SRC = 'https://api.github.com/search/repositories?q='
USR = 'https://api.github.com/users/'
TERM = 'Add your search term here'
LNG = 'Add a programming language here'

## Search for a term
url = '%s%s' % (SRC, TERM)

## Search for a term and a language
url = '%s%s+language:%s' % (SRC, TERM, LNG)

'''
Without authentication the rate limit of the search API is 30.
Skip this part if you have a token.
'''

## Open the JSON data without authentication 
git = ur.urlopen(url).read()
print(type(git))

## Decode the JSON data
de_git = json.loads(git.decode('utf-8'))
print(type(de_git))

'''
If you authenticate, the rate limit is 1000 results (repos) per max 100 repo pages.
'''

par  = {'page': 1, 'per_page': 100}
head = {'Authorization':'token %s' % TOKEN}

## Get the JSON data without authentication 
git = requests.get(url, params=par, headers=head)

## Read the JSON data
de_git = git.json()

##########################################
### Creating lists from the JSON data  ###
##########################################

## List​ the JSON users
users = list([item['owner']['login'] for item in de_git['items']])
print(users)


## List the number of forks / project and count their frequency 
forks = list([item['forks'] for item in de_git['items']])
print(forks)

counter = collections.Counter(forks)
print(counter)

#############################################
### Building a dictionary with usernames ###
#############################################

usersDict = {}    # This creates an empty dictionary

for item in de_git['items']:
    usersDict[item['id']] = list([{'name':item['name']}, {'language':item['language']}, {'username':item['owner']['login']}, {'url':item['owner']['url']}])

'''
If you re-run the for loop, it will add the items to the dictionary, bc. it uses unique repo ids
'''

#######################################
### Call the API for more user info ###
#######################################

'''
Note: This API has a limit as well. 
'''

for repository in usersDict:
    user_name = usersDict[repository][0]['username']
    user_url = '%s%s' % (USR, user_name)
    user_git = ur.urlopen(user_url).read()
    de_user_git = json.loads(user_git.decode('utf-8'))
    usersDict[repository].append({'repos': de_user_git['public_repos']}) #Stores the new information in the dict


'''
Auth version of the API call. 
'''

for repository in usersDict:
    user_name = usersDict[repository][0]['username']
    user_url = '%s%s' % (USR, user_name)
    user_git = requests.get(user_url, headers=head)
    de_user_git = user_git.json()
    usersDict[repository].append({'repos': de_user_git['public_repos']}) #Stores the new information in the dict


