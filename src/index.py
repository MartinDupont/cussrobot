import random
import twitter
import os
from make_tweets.make_tweets import make_tweet

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

def generate_reply():
    is_valid = False
    while not is_valid:
        tweet = make_tweet()
        is_valid = (len(tweet) < 240) and not ("MENTIONHERE" in tweet)
    return tweet

def sub_mentions(template, followers):
    old = ""
    new = template.replace('MENTIONHERE ', 'MENTIONHERE')
    while old != new:
        next_follower = random.choice(followers)
        old = new
        new = new.replace('MENTIONHERE', next_follower, 1)
    return new


def lambda_handler(event_json, context):

    last_tweet_id = api.GetUserTimeline(count=1)[0].id

    followers = api.GetFollowers()
    follower_handles = ["@{}".format(f.screen_name) for f in followers]

    new_mentions = api.GetMentions(since_id=last_tweet_id)
    for mention in new_mentions:
        # api.PostUpdate(generate_insult(follower_handles), in_response_to_status_id=mention)
        api.PostUpdate(generate_reply(), in_response_to_status_id=mention.id)

    status = api.PostUpdate(generate_reply())
    print(status.text)
