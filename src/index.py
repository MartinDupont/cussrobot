import random
import twitter
import os

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

def lambda_handler(event_json, context):
    tweet_text = "Random tweet number: {}".format(random.randint(0, 10000))
    print(tweet_text)
