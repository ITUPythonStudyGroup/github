import requests, re
from myLib import *
from bokeh.charts import Step, show, output_file

"""
Shows the recent push activity of a single given user on a histogram.

TODO
- Support multiple graphs that show pushes by day of the week, other scales of time (minute, second).
"""

# Declare variables
USER = "QuiGonSwag" # TODO Change this to see different users' graphs.

eventCount = [0] * 24
hours = []
for i in range(24):
    hours.append(i*100)
outputFileStr = "pushesByHour-%s" % (USER)
graphTitle = "Pushes By Hour - user: %s" % (USER)


# Fetch a list of public user events
url = '%s/users/%s/events/public' % (BASE, USER)
events = requests.get(url).json()

# Iterate through events and increment values in the eventCount list when a push occurs.
for event in events:
    # Get only push events.
    if event["type"] == "PushEvent":
        # Shorten full time listed (e.g. "2016-03-08T15:30:28Z") to isolate the hour.
        time = event["created_at"][11:13]
        eventCount[int(time)] += 1

# Make a histogram with...
# eventCount as the data,
# "hour" as the printed value listed on the graph,
# 24 as the number of columns drawn,
# cyan as the color of the bars drawn,
# graphTitle as the printed title over the graph.
p = Step(eventCount, xlabel='hours', ylabel='pushes', color='cyan', title=graphTitle)
output_file(outputFileStr)

show(p)

print eventCount
