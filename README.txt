WordleBot.py

This is a Python program that will attempt to complete the Wordle of the day when run. It uses Edge as the browser,
so you must have that browser available. It uses Selenium and Webdriver Manager to interact with Edge, so those
must be downloaded as well.

The program works by putting together random letters until it comes up with a word the the game will accept.
Once it does, it will move on to the next guess and it will also put the word that it guessed into a file
for later use. It can use these words on the 2nd, 3rd and 4th guesses if they fit in with the Wordle hints.
Right now, the bot uses completely random letters, but I am planning on making it so that it can learn from 
the words that it has already guessed to maybe help it make certain letters more common.

When you start the program, it will ask you if you want to play the Wordle or look at history. If you type "play",
and you have not done the Wordle on the day, it will start doing the Wordle. If you have done the Wordle, it will
ask you if you would like to retry the Wordle. If you choose to retry, it will delete the data from the previous play
on the day and start playing the Wordle again. If you type "history", it will ask for a date. If the format is not correct,
it will ask for a date again. If there is no data from that date, it will ask again. If there is data from that date, it will 
display all the guesses, the correct answer, whether or not the bot got it, and the number of guesses that it took.