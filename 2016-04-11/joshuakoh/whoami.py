import requests, re
import json, os
import urllib, cStringIO
import operator
from datetime import datetime as dt
from datetime import timedelta
import random


USER = "joshuakoh" # TODO Change this to see different users' graphs.
GHA_TOKEN = os.environ['GHA_TOKEN']
user_url = "https://api.github.com/users/%s" % USER

def github(path):
    return requests.get(
        url='%s' % (path),
        headers={
            'Authorization': 'token %s' % GHA_TOKEN,
            'User-Agent': 'PSG',
        }
    )

data_users = github(user_url).json()

print "%s is a" % USER,

# If 0 stars, "dark"
# If 0-10 stars, "glittering"
# If >10 stars, "sparkling"
data_starred = github(data_users["starred_url"][:-15]).json()
stars = len(data_starred)
if (stars == 0):
    print "dark,",
elif (stars > 0 and stars <= 10):
    print "glittering,",
else:
    print "sparkling,",

# If 0-10 followers, "mysterious"
# If 11-50 followers, "attractive"
# If >51 followers, "famous"
data_followers = github(data_users["followers_url"]).json()
followers = len(data_followers)
if (followers == 0):
    print "mysterious,",
elif (followers > 0 and followers <= 50):
    print "attractive,",
else:
    print "famous,",

# If 0-10 following, "loner"
# If 11-50 following, "explorer"
# If >51 following, "social"
data_following = github(data_users["following_url"]).json()
following = len(data_following)
if (following == 0):
    print "loner,",
elif (following > 0 and following <= 50):
    print "exploring,",
else:
    print "social,",

# If 0 organizations, "disorganized"
# If >0 organizations, "organized"
data_orgs = github(data_users["organizations_url"]).json()
orgs = len(data_orgs)
if (orgs == 0):
    print "disorganized,",
else:
    print "organized,",

# If 0-10 gists, "gistless"
# If 10-50 gists, "gisty"
# If >50 gists, "gistful"
data_gists = github(data_users["gists_url"][:-10]).json()
gists = len(data_gists)
if (gists == 0):
    print "gistless,",
elif (gists > 0 and gists <= 50):
    print "gisty,",
else:
    print "gistful,",
# Most gists in language 'L: "L-spouting"
if (gists > 0):
    languages = {}
    for gist in data_gists:
        for file in gist["files"]:
            language = gist["files"][file]["language"]
            if (language not in languages):
                languages[language] = 1
            else:
                languages[language] += 1
    sorted = sorted(languages.items(), key=operator.itemgetter(1), reverse=True)
    if (len(sorted) == 1):
        if (sorted[0][0] == None):
            print "plain-text-spewing",
        else:
            print "%s-spouting" % sorted[0][0],
    else:
        if (sorted[0][0] == None):
            print "plain-text-spewing",
        else:
            print "%s-spouting" % sorted[0][0],
        if (sorted[1][0] == None):
            print "(with plain-text mixed in)",
        else:
            print "(with %s mixed in)" % sorted[1][0],

print "programmer,",

issuesCount = 0
forksCount = 0
wikisCount = 0

# If oldest repo is in the last year, "of budding age"
# If oldest repo is in last three yeras, "mature in age"
# If oldest repot is older tha that, "ancient in age"
data_repos = github(data_users["repos_url"]).json()
if (len(data_repos) == 0):
    print "lacking any life experience",
else:
    oldestDate = dt.now()
    for repo in data_repos:
        # Take care of issue, fork, wiki counting
        issuesCount += int(repo["open_issues_count"])
        forksCount += int(repo["forks_count"])
        if (repo["has_wiki"] == True):
            wikisCount += 1

        # Find oldest repo create date
        createdAt = repo["created_at"]
        repoDT = dt.strptime(createdAt, "%Y-%m-%dT%H:%M:%SZ")
        if repoDT < oldestDate:
            oldestDate = repoDT
    daysSinceFirstRepo = (dt.now() - oldestDate).days
    if (daysSinceFirstRepo <= 365):
        print "of budding age",
    elif (daysSinceFirstRepo <= 1095): # 3 years in days
        print "mature in age",
    else:
        print "ancient in age",

adjectives = ["a surprising", "an alarming", "an exciting", "an unexpected", "a boring", "an unimpressive", "a dreary", "a thrilling", "an astonishing", "an incredible", "a startling"]
print "and coding ever onward with experience with %s" % adjectives[random.randrange(0, len(adjectives))],

# If repos have issues, "n issues"
print "%d issues," % issuesCount,
# If repos have forks, "n forks"
print "%d forks," % forksCount,
# If repos have wikis, "and n wikis"
print "and %d wikis." % wikisCount

