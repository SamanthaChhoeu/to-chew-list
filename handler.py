import json
import news.morning as morning

def get_news(event, context):
    news = morning.morning_news()
    body = {
        "articles": json.dumps(news),
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
