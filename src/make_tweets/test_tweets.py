import unittest

from .make_tweets import make_tweet, tidy_grammar

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
        

if __name__ == "__main__":
    unittest.main()
