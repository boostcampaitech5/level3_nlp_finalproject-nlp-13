import threading
import random
from word_db import today_words

todays_word = [0, 0, 0]

def thread():
    #tt = threading.Timer(10, thread)
    tt = threading.Timer(84400, thread)
    tt.start()
    set_todays_word()

def set_todays_word():
    global todays_word
    words = today_words()
    for i in range(3):
        todays_word[i] = words[i]