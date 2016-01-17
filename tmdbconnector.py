__author__ = 'Peter'

import requests
import json

response=requests.get("http://api.tvmaze.com/search/shows?q=house")

print(response)

json_data=json.loads(response.text)
for item in json_data:
    print("id: " + str(item['show']['id']))
    print("Title: " + item['show']['name'])
    print("Summary: " + item['show']['summary'])
    if(item['show']['network']):
        print("Network: " + item['show']['network']['name'])
    else:
        print("Network: " + item['show']['webChannel']['name'])
    print("Status: " + item['show']['status'])
    print("image: " + item['show']['image']['medium'])
    print(" ")

    test = []
    test.append(
        (
            "test",
             item['show']['network']['name'] if item['show']['network'] else item['show']['webChannel']['name']
        )
    )
    print(test)

