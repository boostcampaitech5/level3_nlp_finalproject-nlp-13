import threading
import random

todays_word = [0, 0, 0]
words = ['Circles','Rainy day','하기나 해','Black','한 페이지가 될 수 있게','입술의 말','산책','둘!셋!','하루종일','LAST DANCE']

def thread():
    #tt = threading.Timer(10, thread)
    tt = threading.Timer(84400, thread)
    tt.start()
    set_todays_word()

def set_todays_word():
    global todays_word
    for i in range(3):
        todays_word[i] = words[random.randint(0, 9)]