from flask import Flask, render_template, request, redirect, url_for, session
from functions import thread, todays_word
from word_db import get_rule, word_dict
    
app = Flask(__name__)
app.secret_key = b'817089'

thread()

@app.route('/', methods=['GET','POST'])
def home():
    session['now'] = 'home'
    user = session['user'] if 'user' in session else ''
    language = session['language'] if 'language' in session else 'kor'
    attend = [True, False] * 50
    return render_template("main.html", lang=language, word1 = todays_word[0], word2 = todays_word[1], word3 = todays_word[2], user=user, attend=attend)

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
    session['now'] = 'word_learning_todays_word'
    user = session['user'] if 'user' in session else ''
    language = session['language'] if 'language' in session else 'kor'

    if request.method == 'POST':
        if 'user_audio' in session:
            session.pop('user_audio')
        if 'user_pronounce' in session:
            session.pop('user_pronounce')
        session['num'] = int(request.form['num'])

    word = todays_word[session['num']]
    word_info = word_dict(word)
    pronounce = word_info['g2p_word']
    rule = [word_info['rule'], get_rule(word_info['rule'])]
    recommend = word_info['recommend']
    #explanation = 단어 설명
    #audio = 단어 발음 음성

    user_audio = session['user_audio'] if 'user_audio' in session else ''
    user_pronounce = session['user_pronounce'] if 'user_pronounce' in session else ''

    return render_template("word_learning.html", user=user, lang=language, word=word, pronounce=pronounce, explanation='수료하면 뭐하지...', audio='../static/src/audio/어른.flac', user_audio=user_audio, user_pronounce=user_pronounce, add=recommend, rule=rule, add_or_today='today')

@app.route('/word_learning_additional_word', methods=['GET','POST'])
def word_learning_additional_word():
    session['now'] = 'word_learning_additional_word'
    user = session['user'] if 'user' in session else ''
    language = session['language'] if 'language' in session else 'kor'

    if request.method == 'POST':
        if 'user_audio' in session:
            session.pop('user_audio')
        if 'user_pronounce' in session:
            session.pop('user_pronounce')
        session['word'] = request.form['word']

    word = session['word']
    word_info = word_dict(word)
    pronounce = word_info['g2p_word']
    rule = [word_info['rule'], get_rule(word_info['rule'])]
    #explanation = 단어 설명
    #audio = 단어 발음 음성

    user_audio = session['user_audio'] if 'user_audio' in session else ''
    user_pronounce = session['user_pronounce'] if 'user_pronounce' in session else ''

    return render_template("word_learning.html", user=user, lang=language, word=word, pronounce=pronounce,explanation='나도 9900억 받고 싶다...', audio='../static/src/audio/0310.mp3', user_audio=user_audio, user_pronounce=user_pronounce, add=todays_word, rule=rule, add_or_today='add')

@app.route('/go_prev_word', methods=['GET','POST'])
def go_prev_word():
    if session['num'] == 0:
        session['num'] = 2
    else:
        session['num'] -= 1
    return redirect(url_for('word_learning_todays_word'))

@app.route('/go_next_word', methods=['GET','POST'])
def go_next_word():
    if session['num'] == 2:
        session['num'] = 0
    else:
        session['num'] += 1
    return redirect(url_for('word_learning_todays_word'))

@app.route('/go_prev_page', methods=['GET','POST'])
def go_prev_page():
    return redirect(url_for('word_learning_todays_word'))

@app.route('/get_user_pronounce', methods=['GET', 'POST'])
def get_user_pronounce():
    if request.method == 'POST':
        if 'file' in request.files:
            audio = request.files['file']
            audio.save('./flask/static/src/user_audio/{user}.wav'.format(user=session['user'] if 'user' in session else ''))
            #session['user_pronounce'] = 모델에서 인식한 사용자 발음
            session['user_pronounce'] = '다너'
            session['user_audio'] = '../static/src/user_audio/{user}.wav'.format(user=session['user'] if 'user' in session else '')
    return redirect(url_for(session['now']))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=40001)