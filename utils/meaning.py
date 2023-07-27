import requests
from bs4 import BeautifulSoup
import urllib
    
def word_meaning(word):
    """
    다음 사전에서 단어의 뜻 크롤링하는 함수
    """
    word = urllib.parse.quote(word)
    
    url = f'https://dic.daum.net/search.do?q={word}'
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        try:
            kor = soup.find('div', {"data-tiara-layer":"word kor"})
            ul = kor.find('ul', {"class":"list_search"})
            li = ul.find('li')
            span = li.find('span', {"class":"txt_search"})
            return span.text
        except:
            return ''
    
import pandas as pd
import numpy as np


data = pd.read_csv('words.csv', index_col = 0)
means = []
word_ = data['word']
for i in word_:
    mean_word = word_meaning(i)
    means.append(mean_word)
    
data['meaning'] = means