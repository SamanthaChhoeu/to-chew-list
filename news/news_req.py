from newsapi import NewsApiClient
from spell import translate

KEY = "5c382368f74c48b18bf495cd990e1bd3"
categories = ['business', 'entertainment', 'general', 'health', 
              'science', 'sports', 'technology']

def news_req(region='au', query=None): 
    # Initiate client 
    client = NewsApiClient(api_key=KEY)

    # Get headlines
    if not query:
        headlines = client.get_top_headlines(country=region, sources='google-news')
    else:
        corrected = translate(query)
        final_category = None
        for category in categories:
            if category.startswith(query) or category.startswith(corrected):
                final_category = category
                break
        if not final_category:
            headlines = client.get_everything(
                q=query, 
                sort_by='relevancy',
                sources='google-news'
            )
        else:
            headlines = client.get_top_headlines(
                category=final_category, 
                country=region, 
            )
    return headlines.get('articles')
