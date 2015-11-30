__author__ = 'Peter'

import requests
import json

response=requests.get("http://api.tvmaze.com/search/shows?q=top+gear")

print(response)

json_data=json.loads(response.text)
for item in json_data:
    print("Title: " + item['show']['name'])
    print("Summary: " + item['show']['summary'])
    print("Network: " + item['show']['network']['name'])
    print("Status: " + item['show']['status'])
    print(" ")
