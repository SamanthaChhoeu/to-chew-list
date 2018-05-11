from news_req import news_req
from spell import translate
import argparse

def filter_news(articles):
    articles = articles[:3]
    keep = {'title', 'url'}
    for index, article in enumerate(articles):
        for key in set(article.keys()) - keep:
            del articles[index][key]
    return articles

def request_news(query=None, region='au'):
    articles = news_req(region, query)
    articles = filter_news(articles)
    return articles

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("region")
    parser.add_argument("--query", "-q")
    args = parser.parse_args()

    print(request_news(region=args.region, query=args.query))
