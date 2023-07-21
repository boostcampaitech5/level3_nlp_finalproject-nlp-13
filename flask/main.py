from flask import Flask, render_template, request

app = Flask(__name__)
lang = 'kor'
user = 'not_user'

@app.route('/', methods=['GET','POST'])
def home():
    global lang
    global user
    if request.method == 'POST':
        lang = request.form['language']

    return render_template("main.html", lang=lang, word1='단어1', word2='단어2', word3='단어3', user=user)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=40001)