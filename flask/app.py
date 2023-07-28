from flask import Flask, render_template, request, redirect, url_for, session, current_app, make_response
from functions import thread, todays_word
from  db import *

# Python standard libraries
import json
import os
import sqlite3

# Third party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from google_login.user import User
from google_login.google_login_db import init_db_command, get_db
    
app = Flask(__name__)
app.secret_key = b'817089'

# thread()
# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", '237000578042-ersra4178bpitdll1bebphfnrkgpaacj.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", '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')
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/', methods=['GET','POST'])
def home():
    
    if not current_user.is_authenticated:
        session['now'] = 'home'
        user = session['user'] if 'user' in session else ''
        language = session['language'] if 'language' in session else 'kor'
        #attend = [True] * 100
        attend = attendance(current_user.email) #check attendance
        return render_template("main.html", lang=language, word1 = todays_word[0], word2 = todays_word[1], word3 = todays_word[2], user=user, attend=attend)   
    
    else:
        user = current_user.name
        email = current_user.email
        global user_email_info
        user_email_info = {'email':email,'user':user} 
        check(user_email_info) #add a new user
        language = session['language'] if 'language' in session else 'kor'
        #attend = [True] * 100
        attend = attendance(email) #check attendance
        return render_template("main.html", lang=language, word1 = todays_word[0], word2 = todays_word[1], word3 = todays_word[2], user=user)


@app.route('/language_select', methods=['GET','POST'])
def language_select():
    if request.method == 'POST':
        session['language'] = request.form['language']
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
    print("AAAA")
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

@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    print('authorization_endpoint:', authorization_endpoint)

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)
    # Send user back to homepage
    return redirect(url_for("home"))



@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)
