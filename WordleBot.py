# Import webdriver from Selenium
from selenium import webdriver

# This will allow the program to type and click
from selenium.webdriver.common.keys import Keys

# This will allow the program to find elements on the page
from selenium.webdriver.common.by import By

# This will allow the program to wait for elements to appear on the page
from selenium.webdriver.support.wait import WebDriverWait

# This will work with WebDriverWait to find the elements
from selenium.webdriver.support import expected_conditions as EC

#This is the actionchain that will allow button presses
from selenium.webdriver.common.action_chains import ActionChains

# This is the webdriver for Microsoft Edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# This is the webdriver for Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# This is the webdriver for Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# from webdriver_manager.chrome import ChromeDriverManager
import time

# To get the current date
from datetime import date

# To allow the program to quit
import sys

# Allows me to randomize the guesses
import random

# Allows us to search our learned words for the correct word patterns
import re


class WordleBot:
    """Class for all the coding for the wordle bot"""

    def __init__(self):
        # Instanciate the driver for Microsoft Edge

        self.letter_dic = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h",
            9: "i",
            10: "j",
            11: "k",
            12: "l",
            13: "m",
            14: "n",
            15: "o",
            16: "p",
            17: "q",
            18: "r",
            19: "s",
            20: "t",
            21: "u",
            22: "v",
            23: "w",
            24: "x",
            25: "y",
            26: "z",
        }
        self.rows = [
            "//div[@aria-label='Row 1']",
            "//div[@aria-label='Row 2']",
            "//div[@aria-label='Row 3']",
            "//div[@aria-label='Row 4']",
            "//div[@aria-label='Row 5']",
            "//div[@aria-label='Row 6']",
        ]
        self.word = ""
        self.absent = []
        self.present = [[], [], [], [], []]
        self.presentAll = []
        self.correct = [None, None, None, None, None]
        self.learnedWords = []
        self.wordleWords = []

    def get_url(self, url):
        """Gets the URL"""

        self.driver.get(url)

    def multi_keys(self, count, key):
        """Press the same key multiple times"""

        for i in range(count):
            self.actions.send_keys(key)
            self.actions.perform()

    def random_word(self):
        """Chooses a random word"""
        word = ""
        for i in range(5):
            letter = self.letter_dic[random.randint(1, 26)]
            while letter in self.absent:
                letter = self.letter_dic[random.randint(1, 26)]
            word += letter

        return word

    def legal_word(self):
        word = self.correct[:]
        guess = ""
        for letter in self.presentAll:
            position = random.randint(0, 4)
            while letter in self.present[position] or word[position] != None:
                position = random.randint(0, 4)
            word[position] = letter

        for i in range(5):
            if word[i] == None:
                rand_letter = self.letter_dic[random.randint(1,26)]
                while rand_letter in self.absent:
                    rand_letter = self.letter_dic[random.randint(1,26)]
                word[i] = rand_letter
        for i in word:
            guess += i
        return guess




    def test_word(self, row):
        """Tests if the word was accepted be Wordle"""

        element = self.driver.find_element(By.XPATH, self.rows[row - 1] + "//div[1]//div[1]")
        if element.get_attribute("data-animation") == "flip-in":
            return True
        elif element.get_attribute("data-animation") == "idle":
            return False

    def guess_words(self, row):
        """Chooses a word to guess and then enters it in the Wordle"""

        run = False
        counter = 0
        learnedWord = self.create_regex(row, "Words.txt")
        if learnedWord == None:
            while not run:
                word = self.legal_word()
                self.actions.send_keys(word)
                self.actions.send_keys(Keys.RETURN)
                self.actions.perform()
                counter += 1
                run = self.test_word(row)
                if not run:
                    self.multi_keys(5, Keys.BACK_SPACE)
            self.wordleWords += [word]
            return word
        else:
            self.actions.send_keys(learnedWord)
            self.actions.send_keys(Keys.RETURN)
            self.actions.perform()
            counter += 1
            self.wordleWords += [learnedWord]
            return learnedWord


    def guess_setup(self, word, row):
        """Sets up the rules for the next guess"""
        for i in range(5):
            element = self.driver.find_element(By.XPATH, self.rows[row - 1] + f"//div[{i + 1}]//div[1]")
            status = element.get_attribute("data-state")
            if status == "absent" and word[i] not in self.absent:
                self.absent += [word[i]]
            elif status == "present":
                if word[i] not in self.present[i]:
                    self.present[i] += [word[i]]
                if word[i] not in self.presentAll:
                    self.presentAll += [word[i]]
            elif status == "correct":
                if self.correct[i] == None:
                    self.correct[i] = word[i]
                    if word[i] in self.presentAll:
                        self.presentAll.remove(word[i])

    def win_condition(self, row):
        """Determines if the wordle is complete"""

        for i in range(5):
            element = self.driver.find_element(By.XPATH, self.rows[row - 1] + f"//div[{i + 1}]//div[1]")
            status = element.get_attribute("data-state")
            if status != "correct":
                return False
                break
        return True

    def write_words(self, path, word):
        """Write words into a file"""

        with open(path, 'a') as f:
            f.write(word + "\n")

    def write_wordles(self, path, result):
        """Writes the wordle guesses into the Wordles.txt file"""

        if result == "Loss":
            finalWord = self.driver.find_element(
                By.CLASS_NAME, "Toast-module_toast__iiVsN"
            ).text.lower()
        elif result == "Win":
            finalWord = " " + self.wordleWords[-1]


        with open(path, 'a') as f:
            currentDate = date.today().strftime("%m-%d-%y")
            f.write(currentDate + "\n")
            f.write(result + ":" + " "  + finalWord + "\n")
            for word in self.wordleWords:
                f.write(word + "\n")
            f.write("Number of guesses: " + str(len(self.wordleWords)) + "\n" * 2)

    def delete_wordles(self, path1, path2):
        """Deletes a Wordle entry from the Wordls.txt file if the current date Wordle is in the file"""


        with open(path1, "r+") as f:
            d = f.readlines()
            f.seek(0)
            length = int(d[-2][-2])
            for i in range(len(d) - length - 4):
                f.write(d[i])
            f.truncate()

        with open(path2, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d[:-length]:
                f.write(i)
            f.truncate()


    def wordle_date(self, path):
        """Determines if today's Wordle has been played yet"""

        currentDate = date.today().strftime("%m-%d-%y")

        with open(path, "r") as f:
            d = f.readlines()
            if currentDate + "\n" in d:
                return True
            else:
                return False

    def wordle_done(self, path1, path2):
        """Decides if the Wordle can be done or if it needs to be deleted first"""

        if self.wordle_date(path1):
            while True:
                x = input("Would you like to retry the Wordle today? (y/n)")
                if x == "y":
                    self.delete_wordles(path1, path2)
                    return True
                elif x == "n":
                    return False
                elif x == "x":
                    sys.exit()
                else:
                    print("Invalid option.")
        else:
            return True



    def create_regex(self, row, path):
        """Creates the regular expression to be used to find words in the learned words"""

        if row not in (1, 5, 6):
            regex = [x if x != None else "[a-z]" for x in self.correct]
            for x in range(5):
                for y in self.present[x]:
                    if self.correct[x] == None:
                        if "^" not in regex[x]:
                            regex[x] = regex[x][:-1] + "^" + y + "]"
                        else:
                            regex[x] = regex[x][:-1] + y + "]"
            regexStr = ''.join(regex)
            random.shuffle(self.learnedWords)
            wordStr = ' '.join(self.learnedWords)
            matches = re.findall(regexStr, wordStr)
            Flag1 = False
            Flag2 = False
            for word in matches:
                for i in range(5):
                    if self.correct[i] == None:
                        if word[i] in self.absent and word not in self.presentAll:
                            Flag1 = False
                            break
                else:
                    Flag1 = True
                if Flag1 == True:
                    if self.presentAll != []:
                        for x in self.presentAll:
                            if x not in word:
                                Flag2 = False
                                Flag1 = False
                                break
                        else:
                            Flag2 = True
                    else:
                        Flag2 = True
                if Flag1 == True and Flag2 == True:
                    return word
            return None


    def try_words(self, path):
        """Attempts to try a word form the file Words.txt if it fits within the rules"""

        if self.learnedWords == []:
            with open(path, 'r') as f:
                for line in f:
                    self.learnedWords += [line.strip()]

    def mode(self):
        """Determines if the bot will play the Wordle or go into history mode"""

        print("Enter 'x' at any time to quit.")
        while True:
            x = input("Would you like to play the Wordle or look at history? (play/history)")
            if x == "play":
                return True
            elif x == "history":
                return False
            elif x == "x":
                sys.exit()
            else:
                print("Invalid option.")

    def choose_browser(self):
        """Lets the user choose their preferred browser"""

        while True:
            x = input("What browser would you like to use? (edge/chrome/firefox)")
            if x == "edge":
                try:
                    self.driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()))
                    break
                except:
                    print("Microsoft Edge driver did not work")
            elif x == "chrome":
                try:
                    self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                    break
                except:
                    print("Chrome driver did not work")
            elif x == "firefox":
                try:
                    self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
                    break
                except:
                    print("Firefox driver did not work")
            elif x == "x":
                sys.exit()


    def history(self, path):
        """Enter a date to see the result of that day's Wordle"""

        result = "\n"
        pattern = re.compile("[\d][\d]-[\d][\d]-[\d][\d]")
        while True:
            x = input("Enter a date: (mm-dd-yy)")
            if pattern.match(x) != None:
                try:
                    with open(path, "r") as f:
                        d = f.readlines()
                        for i in d[d.index(x + "\n"):]:
                            result += i
                            if i == "\n":
                                print(result)
                                break
                except:
                    print("No Wordle record for that date.")
            elif x == "x":
                sys.exit()



    def play(self):
        """incorporates previous methods in order to play the whole wordle game"""

        self.try_words("Words.txt")
        time.sleep(2)
        for i in range(1, 7):
            self.word = self.guess_words(i)
            time.sleep(3)
            self.write_words("Words.txt", self.word)
            if self.win_condition(i):
                self.write_wordles("Wordles.txt", "Win")
                break
            self.guess_setup(self.word, i)
            self.create_regex(i, "Words.txt")
        else:
            time.sleep(2)
            self.write_wordles("Wordles.txt", "Loss")

    def setup(self):
        """Does the commands that gets to the point the wordle can be played"""

        self.choose_browser()
        self.actions = ActionChains(self.driver)
        self.get_url("https://www.nytimes.com/games/wordle/index.html")
        try:
            element = self.driver.find_element(
                By.XPATH, "//button[text() = 'Continue']"
            )
            element.click()
        except:
            pass
        element = self.driver.find_element(By.XPATH, "//button[text() = 'Play']")
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "Modal-module_closeIcon__TcEKb")
            )
        )
        element.click()



    def run(self):
        """Run the wordle bot"""

        if self.mode():
            if self.wordle_done("Wordles.txt", "Words.txt"):
                self.setup()
                self.play()
                time.sleep(5)
            else:
                print("Goodbye")
        else:
            self.history("Wordles.txt")

    def test(self):
        """Test method"""

        self.history("Wordles.txt")




if __name__ == "__main__":
    Bot = WordleBot()
    Bot.run()
