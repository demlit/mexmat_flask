from flask import render_template, request, session, url_for, redirect
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
    return render_template("testpage.html")


@app.route('/registration', methods=["GET", "POST"])
def registration_page():
    return render_template("registration.html")


@app.route('/login', methods=["GET", "POST"])
def login_page():
    error = ''
    if request.method == "POST":
        print(request.form)
        login = request.form['login']
        password = request.form['password']
        user = db.get_user(login, password)
        if user:
            session['user'] = user
            return redirect(url_for('testpage'))
        else:
            error += 'User not found'
    return render_template("login.html", error=error)


@app.route('/', methods=["GET", "POST"])
def main_page():
    return render_template("main.html")


if __name__ == '__main__':
    db = database_manage.DB(DB_FILE)
    app.debug = True
    app.run()
