import unittest, random, re
from WordleBot import WordleBot

class TestWordleBot(unittest.TestCase):

    def setUp(self):
        global W
        W = WordleBot()

    def tearDown(self):
        global W
        del W

    def test_random_word(self):

        test = W.random_word()
        pattern = re.compile("[a-z][a-z][a-z][a-z][a-z]")
        self.assertTrue(pattern.match(test) != None)


if __name__ == "__main__":
    unittest.main()

