from morning import morning_news
import sys

categories = {"top": "h", "world": "w", "business": "b", "nation": "n", "science": "t", "tech": "tc", "election": "el", "politics": "p", "entertainment": "e", "sport": "s", "health": "m"}

def parse_input(query=None, region='au'):
    global categories

    if query == None:
        query = sys.argv[1]

    if region == None:
        region = sys.argv[2]

    """
    corrected = translate(query)
    url = "https://api.datamuse.com/words?rel_trg=" + corrected
    response = json.loads(requests.get(url).content.decode())
    category = None

    
    for related in response:
        if related["word"] in categories:
            query = categories[related["word"]]
    """

    if query.lower() in categories:
        query = categories[query]
        result = morning_news(category=query, region=region)
    else:
        result = morning_news(query=query, region=region)

    return result

    #articles = news_req(region, query)

if __name__ == "__main__":
    x = input()
    y = input()
    print(parse_input(x, y))
    #print(parse_input())