import requests
import json

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
      print(line)