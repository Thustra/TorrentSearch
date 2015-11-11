__author__ = 'Peter'

import requests
import json

response=requests.get("http://api.tvmaze.com/search/shows?q=girls")

json_data=json.loads(response.text)

print