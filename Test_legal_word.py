import unittest, random, re
from WordleBot import WordleBot

class TestWordleBot(unittest.TestCase):

    def setUp(self):
        global W
        W = WordleBot()

    def tearDown(self):
        global W
        del W

    def test_legal_word(self):

        W.correct = ["f", None, None, None, "l"]
        W.present = [[], ["c", "v"], ["k"], [], []]
        W.present_all = ["c", "v", "k"]
        W.absent = ["b", "p"]
        test = W.legal_word()
        for i in W.absent:
            self.assertTrue(i not in test)
        pattern = re.compile("f[kvc][kvc][kvc]l")
        self.assertTrue(pattern.match(test) != None)


if __name__ == "__main__":
    unittest.main()

