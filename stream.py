import requests
import json
import ast

url = "https://api.twitter.com/2/tweets/search/stream"
payload={}
headers = {
  'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAA66iwEAAAAAbZtdwOgdYQCUNzPRVopb%2F15CnjQ%3D5iGK97uwYF461cOrCaNZ2tQqAHAHVLVeGBkvcsofaa4TSDKLtm',
  'Content-Type': 'application/json',
  'Cookie': 'guest_id=v1%3A166921382095182903'
}

# response = requests.request("GET", url, headers=headers, data=payload)
with requests.get(url, headers=headers, data=payload, stream=True) as r:
  for line in r.iter_lines():
    if line:
      line = ast.literal_eval(line.decode('utf-8'))
      text = line['data']['text']
      matching_rule = line['matching_rules'][0]['id']
      a = line
      break
print(a)