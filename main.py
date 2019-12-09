from flask import render_template, request, session, url_for, redirect, escape
from flask import Flask
import database_manage

app = Flask(__name__)
DB_FILE = 'db.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/results', methods=["GET", "POST"])
def results_page():
    status = ''
    questions = db.get_questions()
    true_answers = []
    user_answers = []
    for question in questions:
        question_answers = db.get_answers(question['id'])
        for question_answer in question_answers:
            if question_answer['is_right'] == 'TRUE':
                true_answers.append(question_answer)
            if (str(question_answer['question_id']) in session) and (str(question_answer['id']) ==
                                                                     session[str(question_answer['question_id'])][0]):
                user_answers.append(question_answer)
    return render_template("results.html", questions=questions, true_answers=true_answers, user_answers=user_answers,
                           status=status)


@app.route('/testpage', methods=["GET", "POST"])
def test_page():
    status = ''
    if request.method == "POST":
        for answer in request.form:
            session[answer] = request.form.getlist(answer)
    try:
        question_number = escape(session['q'])
    except KeyError:
        question_number = 0
    try:
        question = db.get_next_question(question_number)
    except IndexError:
        return redirect(url_for('results_page'))
    answers = db.get_answers(question['id'])
    answer_type = db.get_answer_type(question['id'])
    session['q'] = question['id']
    return render_template("testpage.html", question=question, answer_type=answer_type, answers=answers, status=status)


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
    session.clear()
    return render_template("login.html", status=status)


@app.route('/', methods=["GET", "POST"])
def main_page():
    return render_template("main.html")


if __name__ == '__main__':
    db = database_manage.DB(DB_FILE)
    app.debug = True
    app.run()
