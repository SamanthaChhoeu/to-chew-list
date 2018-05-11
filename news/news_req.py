import sys,re,json,pprint
import requests

KEY = "5c382368f74c48b18bf495cd990e1bd3"
SITE = "https://newsapi.org/"

REGION = "us"


headline_req = SITE + "v2/top-headlines" + "?country=" + REGION + "&apiKey=" + KEY
headline_data = requests.get(headline_req)

if (headline_data.status_code == 200):
    headline = headline_data.content.decode("utf-8")
    headline = json.loads(headline)
else:
    if (headline_data.status_code == 404):
        sys.exit("DOES_NOT_EXIST: " + str(headline_data.status_code))
    else:
        sys.exit("BAD_REQUEST: " + str(headline_data.status_code))

print(json.dumps(headline))