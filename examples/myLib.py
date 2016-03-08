import requests, re

BASE = 'https://api.github.com'
ORG = 'ITUPythonStudyGroup'

def strip_url_parameters(url):
    return re.sub(r'\{.*\}', '', url)
