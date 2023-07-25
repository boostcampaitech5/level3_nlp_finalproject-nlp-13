from flask import Flask, render_template, request, redirect, url_for, session
import os
from functions import thread, todays_word
    
app = Flask(__name__)
app.secret_key = b'817089'

thread()

@app.route('/', methods=['GET','POST'])
def home():
    session['now'] = 'home'
    user = session['user'] if 'user' in session else ''
    language = session['language'] if 'language' in session else 'kor'

    if 'user_audio' in session:
        session.pop('user_audio')
    if 'user_pronounce' in session:
        session.pop('user_pronounce')

    return render_template("main.html", lang=language, word1 = todays_word[0], word2 = todays_word[1], word3 = todays_word[2], user=user)

@app.route('/language_select', methods=['GET','POST'])
def language_select():
    if request.method == 'POST':
        session['language'] = request.form['language']
    return redirect(url_for(session['now']))

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        ID = request.form['ID']
        PW = request.form['PW']
        
    #계정 확인 & 계정 전환 로직
    session['user'] = ID
    return redirect(url_for(session['now']))

@app.route('/sign_out', methods=['GET','POST'])
def sign_out():
    if request.method == 'POST':
        session.pop('user')
    return redirect(url_for(session['now']))

@app.route('/word_learning_todays_word', methods=['GET','POST'])
def word_learning_todays_word():
    session['now'] = 'word_learning'
    user = session['user'] if 'user' in session else ''
    language = session['language'] if 'language' in session else 'kor'
    
    if request.method == 'POST':
        session['word'] = todays_word[int(request.form['num'])]

    word = session['word']
    #pronounce = 단어의 발음기호
    #explanation = 단어 설명
    #audio = 단어 발음 음성

    user_audio = session['user_audio'] if 'user_audio' in session else ''
    user_pronounce = session['user_pronounce'] if 'user_pronounce' in session else ''

    return render_template("word_learning.html", user=user, lang=language, word=word, pronounce='다너',explanation='단어가 단어지 뭐임', audio='../static/src/audio/0310.mp3', user_audio=user_audio, user_pronounce=user_pronounce, add=['square','저녁하늘','너도'])

@app.route('/get_user_pronounce', methods=['GET', 'POST'])
def get_user_pronounce():
    if request.method == 'POST':
        if 'file' in request.files:
            audio = request.files['file']
            audio.save('./flask/static/src/user_audio/{user}.wav'.format(user=session['user'] if 'user' in session else ''))

            #session['user_pronounce'] = 모델에서 인식한 사용자 발음
            session['user_pronounce'] = '다너'
            session['user_audio'] = '../static/src/user_audio/{user}.wav'.format(user=session['user'] if 'user' in session else '')
    return redirect(url_for('word_learning'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=40001)