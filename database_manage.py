import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DB(object):

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def get_user_by_login(self, login):
        user = self.cursor.execute("SELECT * FROM users WHERE login = '%s'" % login).fetchone()
        return user

    def create_user(self, login, password):
        user = self.get_user_by_login(login)
        if user:
            return 'User already exist'
        self.cursor.execute("INSERT INTO users(login,password) VALUES ('%s', '%s')" % (login, password))
        self.connection.commit()

    def get_questions(self):
        questions = self.cursor.execute("SELECT * FROM questions order by id").fetchall()
        return questions

    def get_next_question(self, q_id):
        question = self.cursor.execute("SELECT * FROM questions where id > %s order by id limit 1" % q_id).fetchall()
        return question[0]

    def get_answers(self, q_id):
        answers = self.cursor.execute("SELECT * FROM answers where question_id=%s" % q_id).fetchall()
        return answers
