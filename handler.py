import json
import news.morning as morning
import news.input as query_handler

def get_news(event, context):
    if event.get('body'):
        payload = json.loads(event['body'])
        news = query_handler.parse_input(payload.get('query'), payload.get('region', 'au'))
    else:
        news = morning.morning_news()
    body = {
        "articles": json.dumps(news)
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
