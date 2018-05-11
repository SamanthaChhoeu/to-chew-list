#!/usr/bin/env python3

import http.client, urllib.parse, json

def translate(news_type):
    text = "Give me {word} news".format(word=news_type)
    data = {'text': text}

    key = 'bda52951d6b14424abf2c671fc518dcd'

    host = 'api.cognitive.microsoft.com'
    path = '/bing/v7.0/spellcheck?'
    params = 'mkt=en-au&mode=spell'

    headers = {'Ocp-Apim-Subscription-Key': key,
    'Content-Type': 'application/x-www-form-urlencoded'}

    conn = http.client.HTTPSConnection(host)
    body = urllib.parse.urlencode (data)
    conn.request ("POST", path + params, body, headers)
    response = conn.getresponse ()
    output = json.loads(response.read().decode())['flaggedTokens']
    output = [suggestion for suggestion in output if suggestion['token'] == news_type]
    if output:
        suggestions = output[0]['suggestions']
        return sorted(suggestions, key=lambda x: x['score'])[0]['suggestion']
    else:
        return news_type

if __name__ == '__main__':
    word = input("Select type of news: ")
    print("You selected {corrected} news".format(corrected=translate(word)))
