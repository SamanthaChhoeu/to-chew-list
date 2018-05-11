from morning import request_news, filter_news
from news_req import news_req
import requests
from spell import translate
import sys, json

categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

def parse_input(query=None, region='au'):
    global categories

    if query == None:
        query = sys.argv[1]

    if region == None:
        region = sys.argv[2]

    corrected = translate(query)
    url = "https://api.datamuse.com/words?rel_trg=" + corrected
    response = json.loads(requests.get(url).content.decode())
    category = None

    for related in response:
        if related["word"] in categories:
            category = related["word"]

    articles = news_req(region, category)

    """
    i = 0
    output = []
    for article in articles:
        if article["description"] != None and query in article["description"]:
            output.append(article)
            i += 1
        if i == 3:
            break

    for j in range(i,3):
        output.append(articles[j-i])
    """

    return filter_news(articles)

if __name__ == "__main__":
    x = input()
    y = input()
    print(parse_input(x, y))
    #print(parse_input())