import re
import requests
import html

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
    for title, link in zip(findall('title', text), findall('link', text)):
        link = re.sub(r".*url=(.*)$", r"\1", link)
        if not(link.startswith('https://news.google.com/news')):
            articles.append({'title': html.unescape(title), 'link': link})
    return articles
