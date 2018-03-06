import requests, re
import json, os
import urllib, cStringIO
import operator
from datetime import datetime as dt
from datetime import timedelta
import random

def github(path):
    return requests.get(
        url='%s' % (path),
        headers={
            'Authorization': 'token %s' % GHA_TOKEN,
            'User-Agent': 'PSG',
        }
    )

USER = "lukebaggett" # TODO Change this to see different users' graphs.
GHA_TOKEN = os.environ['GHA_TOKEN']

user_url = "https://api.github.com/users/%s" % USER

data_users = github(user_url).json()

# Initialize HTML document
temp_str = "whoIs%s.html" % USER
html_doc = open(temp_str, "w")


# Print basic HTML opening
temp_str = "<!DOCTYPE html>\n<html>\n<head>\n<title>Who is %s?" % USER
temp_str += """</title>
<style>body {background-color:#191F24;}
p {font-size:40px;
color:white;
margin-left:50px;
margin-right:700px;}
a {color:yellow;
text-decoration:none;}
a:hover {color: red;
position: relative;}
a[title]:hover:after {
content: attr(title);
padding: 4px 8px;
color: #450000;
position: absolute;
left: 0;
top: 100%;
z-index: 20;
 white-space: nowrap;
-moz-border-radius: 5px;
-webkit-border-radius: 5px;
border-radius: 5px;
-moz-box-shadow: 0px 0px 4px #222;
-webkit-box-shadow: 0px 0px 4px #222;
box-shadow: 0px 0px 4px #222;
background-size: 200px;
background-image: -moz-linear-gradient(top, #eeeeee, #cccccc);
background-image: -webkit-gradient(linear,left top,left bottom,color-stop(0, #eeeeee),color-stop(1, #cccccc));
background-image: -webkit-linear-gradient(top, #eeeeee, #cccccc);
background-image: -moz-linear-gradient(top, #eeeeee, #cccccc);
background-image: -ms-linear-gradient(top, #eeeeee, #cccccc);
background-image: -o-linear-gradient(top, #eeeeee, #cccccc);}
</style>
</head>
<body>
<p>"""
html_doc.write(temp_str)

temp_str = "<a href=\"http://github.com/%s\">%s</a> is a " % (USER, USER)
html_doc.write(temp_str)

# If 0 stars, "dark"
# If 0-10 stars, "glittering"
# If >10 stars, "sparkling"
data_starred = github(data_users["starred_url"][:-15]).json()
stars = len(data_starred)
if (stars == 0):
    html_doc.write("<a href=\"#\" title=\"This user has 0 stars\">dark</a>, ")
elif (stars > 0 and stars <= 10):
    html_doc.write("<a href=\"#\" title=\"This user has up to 10 stars\">glittering</a>, ")
else:
    html_doc.write("<a href=\"#\" title=\"This user has more than 10 stars\">sparkling</a>, ")

# If 0-10 followers, "mysterious"
# If 11-50 followers, "attractive"
# If >51 followers, "famous"
data_followers = github(data_users["followers_url"]).json()
followers = len(data_followers)
if (followers == 0):
    html_doc.write("<a href=\"#\" title=\"This user has very few followers\">mysterious</a>, ")
elif (followers > 0 and followers <= 50):
    html_doc.write("<a href=\"#\" title=\"This user has up to 50 followers\">attractive</a>, ")
else:
    html_doc.write("<a href=\"#\" title=\"This user has more than 50 followers\">famous</a>, ")

# If 0-10 following, "loner"
# If 11-50 following, "venturing"
# If >51 following, "social"
data_following = github(data_users["following_url"]).json()
following = len(data_following)
if (following == 0):
    html_doc.write("<a href=\"#\" title=\"This user is following very few other users\">loner</a>, ")
elif (following > 0 and following <= 50):
    html_doc.write("<a href=\"#\" title=\"This user is following up to 50 other users\">venturing</a>, ")
else:
    html_doc.write("<a href=\"#\" title=\"This user is following more than 50 other users\">social</a>, ")

# If 0 organizations, "disorganized"
# If >0 organizations, "organized"
data_orgs = github(data_users["organizations_url"]).json()
orgs = len(data_orgs)
if (orgs == 0):
    html_doc.write( "<a href=\"#\" title=\"This user is not a member of an organization\">disorganized</a>, ")
else:
    html_doc.write( "<a href=\"#\" title=\"This user is a member of an organization\">organized</a>, ")

# If 0-10 gists, "gistless"
# If 10-50 gists, "gisty"
# If >50 gists, "gistful"
data_gists = github(data_users["gists_url"][:-10]).json()
gists = len(data_gists)
if (gists == 0):
    html_doc.write( "<a href=\"#\" title=\"This user has made very few gists\">gistless</a>, ")
elif (gists > 0 and gists <= 50):
    html_doc.write( "<a href=\"#\" title=\"This user has made up to 50 gists\">gisty</a>, ")
else:
    html_doc.write( "<a href=\"#\" title=\"This user has made more than 50 gists\">gistful</a>, ")
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
            html_doc.write("<a href=\"#\" title=\"This user has the most gists in this language\">plain-text-spewing</a> ")
        else:
            temp_str = "<a href=\"#\" title=\"This user has the most gists in this language\">%s-spouting</a> " % sorted[0][0]
            html_doc.write(temp_str)
    else:
        if (sorted[0][0] == None):
            html_doc.write("<a href=\"#\" title=\"This user has the most gists in this language\">plain-text-spewing</a> ")
        else:
            temp_str = "<a href=\"#\" title=\"This user has the most gists in this language\">%s-spouting</a> " % sorted[0][0]
            html_doc.write(temp_str)
        if (sorted[1][0] == None):
            html_doc.write("<a href=\"#\" title=\"This user has the second most gists in this language\">(with plain-text mixed in)</a> ")
        else:
            temp_str = "<a href=\"#\" title=\"This user has the second most gists in this language\">(with %s mixed in)</a> " % sorted[1][0]
            html_doc.write(temp_str)


html_doc.write("programmer, ")

issuesCount = 0
forksCount = 0
wikisCount = 0

# If oldest repo is in the last year, "of budding age"
# If oldest repo is in last three yeras, "mature in age"
# If oldest repot is older tha that, "ancient in age"
data_repos = github(data_users["repos_url"]).json()
if (len(data_repos) == 0):
    html_doc.write("<a href=\"#\" title=\"This user has not pushed any repos\">lacking any life experience</a> ")
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
        html_doc.write("<a href=\"#\" title=\"This user's first repo push was made within the last year\">of budding age</a> ")
    elif (daysSinceFirstRepo <= 1095): # 3 years in days
        html_doc.write("<a href=\"#\" title=\"This user's first repo push was made within the last three years\">mature in age</a> ")
    else:
        html_doc.write("<a href=\"#\" title=\"This user's first repo push was made more than three years ago\">ancient in age</a> ")

adjectives = ["a surprising", "an alarming", "an exciting", "an unexpected", "a boring", "an unimpressive", "a dreary", "a thrilling", "an astonishing", "an incredible", "a startling"]
temp_str = "and coding ever onward with their backpack full of %s " % adjectives[random.randrange(0, len(adjectives))]
html_doc.write(temp_str)

# If repos have issues, "n issues"
temp_str = "<a href=\"#\" title=\"This user's repos' total active issue count\">%d issues</a>, " % issuesCount
html_doc.write(temp_str)
# If repos have forks, "n forks"
temp_str = "<a href=\"#\" title=\"This user's repos' total forks count\">%d forks</a>, " % forksCount
html_doc.write(temp_str)
# If repos have wikis, "and n wikis"
temp_str = "and <a href=\"#\" title=\"This user's repos' total wikis count\">%d wikis</a>. " % wikisCount
html_doc.write(temp_str)

# Print basic HTML closing
html_doc.write("</p>\n</body>\n</html>")

html_doc.close()