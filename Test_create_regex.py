import unittest, random, re
from WordleBot import WordleBot

class TestWordleBot(unittest.TestCase):

    def setUp(self):
        global W
        W = WordleBot()

    def tearDown(self):
        global W
        del W

    def test_create_regex(self):

        W.learned_words = ["hello", "jello", "crane" "bgakj"]
        W.correct = [None, "g", None, "k", None]
        W.present = [["a"], [], ["b", "j"], [], []]
        W.present_all = ["a", "b", "j"]
        W.absent = ["h", "z", "x"]
        test = W.create_regex(2)
        print(test)
        self.assertTrue(test == "bgakj")


if __name__ == "__main__":
    unittest.main()

