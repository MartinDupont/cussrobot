import unittest

from .make_tweets import make_tweet, tidy_grammar, pick_random, sub_emojis, sub_hashtags

class CheckTweets(unittest.TestCase):

    def test_generate_tweets_without_crashing(self):
        for i in range(0,10):
            make_tweet()
    
    def test_tidy_grammar(self):
        parameters = [
            ('word . word', 'word. word'),
            ('word , word', 'word, word'),
            ('word ? word', 'word? word'),
            ('word ! word', 'word! word'),
            ('word : word', 'word: word'),
            ('word ; word', 'word; word'),
            ('s / o', 's/o'),
            ('dead - ass', 'dead-ass'),
        ]
        for given, expected in parameters:
            result = tidy_grammar(given)
            self.assertEqual(result, expected)
        
    def test_pick_random(self):
        """should return an element from the list"""
        probs = {"a":0.5, "b":0.5}
        for i in range(10):
            result = pick_random(probs)
            self.assertTrue(result in probs.keys())
 
    def test_pick_random_2(self):
        """should handle the trivial case"""
        probs = {"a":1}
        result = pick_random(probs)
        self.assertTrue(result == "a")
           
    def test_sub_emojis(self):
        input_string = "yo this is bad EMOJIHERE "
        distribution = {"&#128514;": 1}
        result = sub_emojis(input_string, distribution)
        self.assertEqual(result, "yo this is bad 😂")
    
    def test_sub_hashtags(self):
        input_string = "yo this is bad HASHTAGHERE "
        distribution = {"#YOLO": 1}
        result = sub_hashtags(input_string, distribution)
        self.assertEqual(result, "yo this is bad #YOLO ")    
    
if __name__ == "__main__":
    unittest.main()
