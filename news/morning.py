from news_req import news_req

def parse_news ():
    articles = news_req("au")
    articles = articles[:3]

    keep = {'title', 'url'}
    for index, article in enumerate(articles):
        for key in set(article.keys()) - keep:
            del articles[index][key]

    print(articles)

    #send to fb api

parse_news()