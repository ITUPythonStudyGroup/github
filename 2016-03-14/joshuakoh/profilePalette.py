import requests, re
import json
from colorthief import ColorThief as CT
import urllib, cStringIO

USER = "joshuakoh" # TODO Change this to see different users' graphs.

userUrl = 'https://api.github.com/users/%s' % (USER)

# userUrl takes the form "https://api.github.com/users/:user"
# does NOT check for 'default' user image (a white square). Check for this by testing if return hex == #040404
def getDominantColor(userUrl):
    userData = requests.get(userUrl).json()
    profileUrl = userData['avatar_url']

    ctPalette = CT(cStringIO.StringIO(urllib.urlopen(profileUrl).read()))
    # get the dominant color
    dominantColorRGB = ctPalette.get_color(quality=1)

    hex = convertRGBtoHex(dominantColorRGB)
    return hex

# rgb is a three element tuple
def convertRGBtoHex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

print getDominantColor(userUrl)
