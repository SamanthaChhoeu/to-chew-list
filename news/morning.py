from news_req import news_req
from spell import translate
import argparse
import requests
import json

def morning_news(category=None, query=None, region='au'):
    articles = news_req(category, region, query)[:3]

    for article in articles:
        article["link"] = shorten_url(article["link"])

    return articles

def shorten_url(longUrl):
    url = "https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyDRc9XUsoGqcVrPKNOCeTsRW_1CEv2Vw8I"
    postdata = {'longUrl':longUrl}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(postdata), headers=headers)
    return r.json()["id"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("region")
    parser.add_argument("--query", "-q")
    args = parser.parse_args()

    print(morning_news(region=args.region, query=args.query))
