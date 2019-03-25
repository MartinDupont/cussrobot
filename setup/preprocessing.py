# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 11:19:09 2019

@author: martin
"""

import re

EMOJI_REGEX = '&#[0-9]*;'
HASHTAG_REGEX = '#(?=\d*[A-Za-z])[\w]*'

UNWANTED_HASHTAGS = ["#iphone", "#xxx", "#ipad", "#porn", "#xxx",
                     "#TheWalkingDead", "#rupaulsdragrace", "#SonsOfAnarchy"
                     "#android", "#XXX", "#AMCWalkingDead"]

BAD_WORDS = [
    "chinaman",
    "chinamen",
    "chink",
    "crip",
    "dago",
    "daygo",
    "dego",
    "dyke",
    "fag",
    "gash",
    "gimp",
    "golliwog",
    "gook",
    "gyp",
    "halfbreed",
    "half-breed",
    "homo",
    "hooker",
    "jap",
    "kike",
    "kraut",
    "lesbo",
    "mandingo",
    "muzzie",
    "negro",
    "nigger",
    "paki",
    "pickaninnie",
    "pickaninny",
    "queer",
    "raghead",
    "retard",
    "shemale",
    "skank",
    "slut",
    "spade",
    "spic",
    "spook",
    "tard",
    "towelhead"
    "trannie",
    "tranny",
    "wetback",
    "whore",
    "wop"
]

EXCLUDED_WORDS = ['het', 'robin', 'valerie', 'spear', 'gooooo', 'je', 'vrijheid']

BORING_EMOJIS = ["&#8220;", "&#8221;", "&#8230;"]

def remove_retweets(text):
    return re.sub('rt MENTIONHERE','', text)


def preprocess(text_string):

    space_pattern = '\s+'
    giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
        '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    mention_regex = '@[\w\-]+:*'
    parsed_text = text_string.lower()
    parsed_text = re.sub(space_pattern, ' ', parsed_text)
    parsed_text = re.sub(giant_url_regex, '', parsed_text)
    parsed_text = re.sub(mention_regex, ' MENTIONHERE ', parsed_text)
    parsed_text = re.sub(EMOJI_REGEX, ' EMOJIHERE ', parsed_text)
    parsed_text = remove_retweets(parsed_text)
    parsed_text = re.sub(HASHTAG_REGEX, ' HASHTAGHERE ', parsed_text)
    parsed_text = re.sub('["\']', '', parsed_text)
    parsed_text = re.sub('&amp', '&', parsed_text)
    parsed_text = re.sub('[\(\)]', '', parsed_text)
    parsed_text = re.sub(space_pattern, ' ', parsed_text).strip() # yes, it is necessary
    return parsed_text


def split_into_words(tweet):
    splitted = re.split('(\W)', tweet)
    return [word for word in splitted if not word in ["", " ", "rt"]]


def get_distribution(tweets, regex, unwanted):
    words = {}
    count = 0
    for tweet in tweets:
        found_words = re.findall(regex, tweet)
        for tag in [t for t in found_words if not t in unwanted]:
            count += 1
            try:
                words[tag]+= 1
            except:
                words[tag] = 1
    return {h: (n*1.0)/count for h, n in words.items()}


def get_emoji_distribution(tweets):
    return get_distribution(tweets, EMOJI_REGEX, BORING_EMOJIS)

    
def get_hashtag_distribution(tweets):
    return get_distribution(tweets, HASHTAG_REGEX, UNWANTED_HASHTAGS)


def find_bad_words(phrase):
    if any(bad in phrase.lower() for bad in BAD_WORDS + EXCLUDED_WORDS):
        return True
    return False

