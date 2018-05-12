import re
import requests
import html
import json
import boto3

def findall(tag, text):
    return re.findall("<{tag}>(.*?)</{tag}>".format(tag=tag), text)

def build_query(region, query=None):
    url = "https://news.google.com/news?output=rss&ned=" + region
    if query:
        url += "&q=" + query
    return url

def build_category(region, category=None):
    url = "https://news.google.com/news?output=rss&ned=" + region
    if category:
        url += "&topic=" + category
    return url

def news_req(category=None, region='au', query=None): 
    if category:
        url = build_category(region, category)
    elif query:
        url = build_query(region, query)
    else:
        url = "https://news.google.com/news?output=rss&topic=h&ned=" + region

    text = requests.get(url).content.decode()
    articles = []
    titles = findall('title', text)
    links = findall('link', text)
    images = ['http:' + link for link in re.findall(r"img src=&quot;(.*?)&quot;", text)]
    for title, link in zip(titles, links):
        link = re.sub(r".*url=(.*)$", r"\1", link)
        if not(link.startswith('https://news.google.com/news')):
            title = html.unescape(title)
            title, subtitle = title.rsplit(' - ', 1)
            articles.append({
                'title': title, 
                'source': subtitle, 
                'link': link, 
                'image': images.pop(0) if images else "" 
            })
    return articles

def get_positive_articles(articles):
    client = boto3.client(service_name='comprehend', region_name='us-east-1')
    def get_positivity(article):
        resp = client.detect_sentiment(Text=article['title'], LanguageCode='en')
        return resp['SentimentScore']['Positive']

    articles.sort(key=get_positivity, reverse=True)
    return articles
