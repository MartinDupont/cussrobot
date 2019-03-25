# -*- coding: utf-8 -*-
import unittest
from setup import preprocessing as pp

class CheckTweets(unittest.TestCase):

    def test_filter_bad_words(self):
        result = pp.find_bad_words("that guy is a nigger")
        self.assertEqual(result, True)
        
    def test_preprocesser(self):
        parameters = [("!!!!!!!!!","!!!!!!!!!"),
         ("@T_Madison_x:", "MENTIONHERE"),
         ("@T_Madison_x", "MENTIONHERE"),
         ("The      thing", "the thing"),
         ("Look here: https://en.wikipedia.org/wiki/Main_Page", "look here:"),
         ("#YOLO", "HASHTAGHERE"),
         ('&amp', '&'),
         ("you are (bad)", "you are bad"),
         ("cool!&#8221;", "cool! EMOJIHERE"),
         ("@T_Madison_x: @elonmusk#SWAGGER&#8221;", "MENTIONHERE MENTIONHERE HASHTAGHERE EMOJIHERE")
         ]
        
        for given, expected in parameters:
            result = pp.preprocess(given)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
