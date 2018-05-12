from .news_req import news_req, get_positive_articles
from .spell import translate
import argparse
import requests
import json

def morning_news(category=None, query=None, region='au', N=3):
    articles = news_req(category, region, query)
    if not query and not category:
        articles = get_positive_articles(articles)

    articles = articles[:N]
    return articles
