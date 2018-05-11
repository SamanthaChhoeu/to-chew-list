import re
import requests
import html

def findall(tag, text):
    return re.findall("<{tag}>(.*?)</{tag}>".format(tag=tag), text)

def build_url(region, query=None):
    url = "https://news.google.com/news?output=rss&ned=" + region
    if query:
        url += "&q=" + query
    return url

def news_req(region='au', query=None): 
    url = build_url(region, query)
    text = requests.get(url).content.decode()
    articles = []
    for title, link in zip(findall('title', text), findall('link', text)):
        link = re.sub(r".*url=(.*)$", r"\1", link)
        if not(link.startswith('https://news.google.com/news')):
            articles.append({'title': html.unescape(title), 'link': link})
    return articles
