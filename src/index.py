import random
import twitter

def lambda_handler(event_json, context):
    tweet_text = "Random tweet number: {}".format(random.randint(0, 10000))
    print(tweet_text)
