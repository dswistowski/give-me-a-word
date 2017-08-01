import json
import random

import config
import words
import urllib.request


def get_random_word():
    while True:
        word = random.choice(words.WORDS)
        definition = get_word_definition(word)
        if definition:
            return definition


def get_word_definition(word):
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + word
    headers = {'app_id': config.OXFORD_APP_ID, 'app_key': config.OXFORD_APP_KEY}
    req = urllib.request.Request(url, None, headers)
    try:
        with urllib.request.urlopen(req) as response:
            return word, \
                   json.loads(response.read().decode('utf-8')).get('results')[0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    except (urllib.error.HTTPError, KeyError):
        return None
