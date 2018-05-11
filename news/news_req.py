from newsapi import NewsApiClient

KEY = "5c382368f74c48b18bf495cd990e1bd3"

def news_req(region, query=None): 
    # Initiate client 
    client = NewsApiClient(api_key=KEY)

    # Get headlines
    if not query:
        headlines = client.get_top_headlines(country=region)
    else:
        headlines = client.get_everything(q=query, country=region)
    return headlines.get('articles')

if __name__ == '__main__':
    print(news_req('au'))
