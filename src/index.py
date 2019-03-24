import random
import twitter
import os
from make_tweets.py import make_tweet

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

def generate_insult(followers):
    is_less_than = False
    while not is_less_than:
        template = make_tweet()
        tweet = sub_mentions(template, followers)
        is_less_than = len(tweet) < 240
    return tweet

def sub_mentions(template, followers):
    old = ""
    new = template.replace('MENTIONHERE ', 'MENTIONHERE')
    while old != new:
        next_hashtag = random.choice(followers)
        old = new
        new = new.replace('MENTIONHERE', next_hashtag, 1)
    return new


def lambda_handler(event_json, context):

    followers = api.GetFollowerIds()

    status = api.PostUpdate(generate_insult(followers))
    print(status.text)
