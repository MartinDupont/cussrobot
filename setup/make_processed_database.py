# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 16:58:52 2019

@author: martin
"""

import pandas as pd
import numpy as np
import pickle
from preprocessing import preprocess, split_into_words, get_emoji_distribution, \
 get_hashtag_distribution, find_bad_words

SOURCE_FOLDER = '../src/make_tweets/'

def get_word_counts(data):
    word_counts = {}
    for tweet in data:
        for word in split_into_words(tweet):
            try:
                word_counts[word] += 1
            except:
                word_counts[word] = 1
    return word_counts

def make_matrix_and_mappings(data):
    word_counts = get_word_counts(data)
    
                
    reduced_vocab = [word for word in word_counts.keys() if word_counts[word] > 2]
    unique_words = ["START"] + reduced_vocab + ["END"]
    
    word_index = {word: i for word, i in zip(unique_words, range(len(unique_words)))}
    reverse_word_index = {index: word for word, index in word_index.items()}
    def get_index(word):
        try:
            return word_index[word]
        except: 
            return None
        
    
    n_words = len(unique_words)
    transition_matrix = np.zeros((n_words, n_words))
    for tweet in data:
        prev_index = get_index("START")
        splitted = split_into_words(tweet) + ["END"]
        for next_word in splitted:
            next_index = get_index(next_word)
            if (next_index is not None) and (prev_index is not None):
                transition_matrix[prev_index, next_index] += 1
            prev_index = next_index
         
    normalization_factors = np.sum(transition_matrix, axis=1)
    normalization_factors[-1] = 1 #END
    norm = np.outer(normalization_factors, np.ones(n_words))
    
    transition_probabilities = transition_matrix / norm
    
    return transition_probabilities, reverse_word_index

if __name__ == "__main__":

    data = pd.read_csv("labeled_data.csv")
    
    data = data[data["offensive_language"] > 1]
    data = data["tweet"][data.apply(lambda x: not find_bad_words(x["tweet"]), axis=1)] 
    
    emoji_distribution = get_emoji_distribution(data)
    hashtag_distribution = get_hashtag_distribution(data)
    
    data = data.apply(lambda x: preprocess(x))
    
    transition_probabilities, reverse_word_index = make_matrix_and_mappings(data)

    pickle.dump(transition_probabilities, open(SOURCE_FOLDER+'transitions.pickle', "wb" ))
    pickle.dump(reverse_word_index, open(SOURCE_FOLDER+'word_index.pickle', "wb" ))
    pickle.dump(emoji_distribution, open(SOURCE_FOLDER+'emojis.pickle', "wb" ))
    pickle.dump(hashtag_distribution, open(SOURCE_FOLDER+'hashtags.pickle', "wb" )) 
    
                         