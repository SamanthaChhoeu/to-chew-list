from news_req import news_req
from spell import translate
import argparse

def morning_news(category=None, query=None, region='au'):
    articles = news_req(category, region, query)
    return articles[:3]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("region")
    parser.add_argument("--query", "-q")
    args = parser.parse_args()

    print(morning_news(region=args.region, query=args.query))
