# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 19:11:10 2019

@author: martin
"""
import random
import numpy as np
import pickle

transition_probabilities = pickle.load(open('transitions.pickle', "rb" ))
reverse_word_index = pickle.load(open('word_index.pickle', "rb" ))
emoji_distribution = pickle.load(open('emojis.pickle', "rb" ))
hashtag_distribution = pickle.load(open('hashtags.pickle', "rb" ))


def generate_tweet_template():
    n_words = len(reverse_word_index.keys())
    word = "START"
    tweet = []
    index = 0
    while word != "END":
        row = transition_probabilities[index, :]
        cumsum = np.cumsum(row)
        randint = random.random()
        for index in range(1, n_words):
            if randint < cumsum[index]:
                break
        word = reverse_word_index[index]
        tweet += [word]
    
    return " ".join(tweet[0:-1])

        
def tidy_grammar(template):
    template = template.replace(' .', '.')
    template = template.replace(' ,', ',')
    template = template.replace(' ?', '?')
    template = template.replace(' !', '!')
    template = template.replace(' :', ':')
    template = template.replace(' ;', ';')
    template = template.replace(' / ', '/')
    template = template.replace(' - ', '-')
    return template

def pick_random(input_dict):
    thing = [(a, b) for a, b in input_dict.items()]
    keys = [x[0] for x in thing]
    values = [x[1] for x in thing]
    cumsum = np.cumsum(values)
    randint = random.random()
    for index in range(0, len(cumsum)):
        if randint < cumsum[index]:
            break
    choice = keys[index]
    return choice

def sub_emojis(template):
    old = ""
    new = template.replace('EMOJIHERE ', 'EMOJIHERE')
    while old != new:
        next_emoji = pick_random(emoji_distribution)
        old = new
        new = new.replace('EMOJIHERE', next_emoji, 1)
    return new

def sub_hashtags(template):
    old = ""
    new = template.replace('HASHTAGHERE ', 'HASHTAGHERE')
    while old != new:
        next_hashtag = pick_random(hashtag_distribution)
        old = new
        new = new.replace('HASHTAGHERE', next_hashtag, 1)
    return new

def is_useless_tweet(tweet):
    conds = [
            tweet == 'MENTIONHERE',
            tweet == 'MENTIONHERE MENTIONHERE',
            len(tweet.split(' ')) == 1,
            tweet.count('MENTIONHERE') > 2
            ]
    if any(conds):
        return True
    return False
    

def make_tweet():
    is_useless = True
    while is_useless:
        template = generate_tweet_template()
        is_useless = is_useless_tweet(template)
    
    template = tidy_grammar(template)
    template = sub_emojis(template)
    return sub_hashtags(template)