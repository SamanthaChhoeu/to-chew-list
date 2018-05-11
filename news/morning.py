import news_req

def core ():
    #article_dict = news_req()
    articles = news_req()
    articles = articles[:3]

    """
    output = {}
    output["articles"] = []

    for i in range(3):
        temp = {}
        temp["title"] = articles[i]["title"]
        temp["description"] = articles[i]["description"]
        temp["url"] = 
        output["articles"][i] = articles[i]
    """

    keep = {'title', 'description', 'url'}
    for index, article in enumerate(articles):
        for key in set(article.keys()) - keep:
            del articles[index][key]

    print(articles)
    #send to fb api