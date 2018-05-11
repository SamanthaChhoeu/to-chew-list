from .morning import morning_news
import sys

categories = {"top": "h", "world": "w", "business": "b", "nation": "n", "science": "t", "tech": "tc", "election": "el", "politics": "p", "entertainment": "e", "sport": "s", "health": "m"}

def parse_input(query=None, region='au'):
    if query and query.lower() in categories:
        result = morning_news(category=categories[query], region=region)
    else:
        result = morning_news(query=query, region=region)
    return result
