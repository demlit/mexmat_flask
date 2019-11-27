from flask import render_template, request, session, url_for, redirect, escape
from flask import Flask
import database_manage

app = Flask(__name__)
DB_FILE = 'db.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/results', methods=["GET", "POST"])
def results_page():
    return render_template("results.html")


@app.route('/testpage', methods=["GET", "POST"])
def test_page():
    status = ''

    if request.method == "POST":
        print(request.form)
    try:
        question_number = escape(session['q'])
    except KeyError:
        question_number = 0
    try:
        question = db.get_next_question(question_number)
    except IndexError:
        return redirect(url_for('results_page'))
    answers = db.get_answers(question['id'])
    print(answers)
    session['q'] = question['id']
    return render_template("testpage.html", question=question, answers=answers, status=status)


@app.route('/registration', methods=["GET", "POST"])
def registration_page():
    status = ''
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        added = db.create_user(login, password)
        if added:
            status += added
        else:
            return redirect(url_for('login_page'))
    return render_template("registration.html", status=status)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    status = ''
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        user = db.get_user_by_login(login)
        if user:
            if user['password'] == password:
                session['user'] = user
                return redirect(url_for('test_page'))
            else:
                status += 'Wrong password'
        else:
            status += 'User not found'
    return render_template("login.html", status=status)


@app.route('/', methods=["GET", "POST"])
def main_page():
    return render_template("main.html")


if __name__ == '__main__':
    db = database_manage.DB(DB_FILE)
    app.debug = True
    app.run()
