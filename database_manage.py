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

    def get_user(self, login, password):
        user = self.cursor.execute("SELECT * FROM users WHERE login = '%s' AND password = '%s'"
                                   % (login, password)).fetchone()
        if user:
            return user
        else:
            return None

    def create_user(self, login, password):
        user = self.get_user(login, password)
        if user:
            return 'Error: user already exist!'
        self.cursor.execute("INSERT INTO users(login,password) VALUES ('%s', '%s')" % (login, password))
        self.connection.commit()
        return self.get_user(login, password)

    def get_question(self):
        pass
