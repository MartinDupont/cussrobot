import random
import twitter
import os
from make_tweets.make_tweets import make_tweet

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

ORIGINAL_TWEET_PROBABILITY = 1.0/60
# Currently operating with being called every 3 minutes. 

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

def generate_insult(ordered_followers):
    is_less_than = False
    first = ordered_followers[0]
    while not is_less_than:
        template = make_tweet()
        tweet = sub_mentions(template, ordered_followers)
        is_less_than = (len(tweet) < 240) and (len(tweet) > 5) and (first in tweet)
    return tweet

def sub_mentions(template, followers):
    old = ""
    new = template.replace('MENTIONHERE ', 'MENTIONHERE')
    follower_iterator = iter(followers)
    while old != new:
        next_follower = next(follower_iterator)
        old = new
        new = new.replace('MENTIONHERE', next_follower+' ', 1)
    return new


def lambda_handler(event_json, context):

    last_tweet_id = api.GetUserTimeline(count=1)[0].id

    followers = api.GetFollowers()
    follower_handles = ["@{}".format(f.screen_name) for f in followers]

    new_mentions = api.GetMentions(since_id=last_tweet_id)
    for mention in new_mentions:
        # api.PostUpdate(generate_insult(follower_handles), in_response_to_status_id=mention)
        first = "@"+mention.user.screen_name
        random.shuffle(follower_handles)
        ordered_followers = [first] + [f for f in follower_handles if not f == first]
        reply = api.PostUpdate(generate_insult(ordered_followers), in_reply_to_status_id=mention.id)
        print(reply)

    if random.random() < ORIGINAL_TWEET_PROBABILITY:
        random.shuffle(follower_handles)
        status = api.PostUpdate(generate_insult(follower_handles))
        print(status.text)
