from morning import request_news, filter_news
from news_req import news_req
import requests
from spell import translate
import sys, json

categories = {"top": "h", "world": "w", "business": "b", "nation": "n", "science": "t", "technology": "tc", "election": "el", "politics": "p", "entertainment": "e", "sport": "s", "health": "m"}

def parse_input(query=None, region='au'):
    global categories

    if query == None:
        query = sys.argv[1]

    if region == None:
        region = sys.argv[2]

    """
    corrected = translate(query)
    url = "https://api.datamuse.com/words?rel_trg=" + corrected
    response = json.loads(requests.get(url).content.decode())
    category = None

    
    for related in response:
        if related["word"] in categories:
            query = categories[related["word"]]
    """

    if query.lower() in categories:
        query = categories[query]
        request_news(category=query, region=region)
    else:
        request_news(query=query, region=region)


    #articles = news_req(region, query)

if __name__ == "__main__":
    x = input()
    y = input()
    print(parse_input(x, y))
    #print(parse_input())