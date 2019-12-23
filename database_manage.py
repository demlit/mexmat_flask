import sqlite3
from urllib.request import pathname2url

database = {
    'users':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('login', 'TEXT NOT NULL'),
            ('password', 'TEXT'),
            ('firstname', 'TEXT'),
            ('lastname', 'TEXT')
        ],
    'questions':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('question', 'TEXT NOT NULL'),
            ('type_id', 'INTEGER'),
            ('', 'FOREIGN KEY(type_id) REFERENCES answer_types(id)')
        ],
    'answers':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('question_id', 'INTEGER NOT NULL'),
            ('answer', 'TEXT NOT NULL'),
            ('is_right', 'NUMERIC NOT NULL DEFAULT FALSE'),
            ('', 'FOREIGN KEY(question_id) REFERENCES questions(id)')
        ],
    'test_results':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('user_id', 'INTEGER NOT NULL'),
            ('date', 'NUMERIC'),
            ('score', 'INTEGER DEFAULT 0'),
            ('', 'FOREIGN KEY(user_id) REFERENCES users(id)')
        ],
    'answer_types':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('type', 'TEXT NOT NULL')
        ]
}

questions = [('1', '"Какое из утверждений верно?"', '1'),
             ('2', '"Какие из утверждений не верны?"', '2'),
             ('3', '"Сколько часов в сутках?"', '3')
             ]

answers = [
    ('1', '"Земля вращается вокруг Луны"', '"FALSE"'),
    ('1', '"Земля вращается вокруг Солнца"', '"TRUE"'),
    ('1', '"Земля вращается вокруг головы"', '"FALSE"'),
    ('2', '"Страусы летают"', '"TRUE"'),
    ('2', '"Страусы плавают"', '"TRUE"'),
    ('2', '"Страусы существуют"', '"FALSE"'),
    ('3', '"24"', '"TRUE"')
]

answer_types = [
    ('1', '"radio"'),
    ('2', '"checkbox"'),
    ('3', '"text"')
]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DB(object):

    def __init__(self, filename):
        try:
            self.connection = sqlite3.connect('file:{}?mode=rw'.format(pathname2url(filename)), check_same_thread=False,
                                              uri=True)
            self.connection.row_factory = dict_factory
            self.cursor = self.connection.cursor()
        except sqlite3.OperationalError:
            self.connection = sqlite3.connect(filename, check_same_thread=False)
            self.connection.row_factory = dict_factory
            self.cursor = self.connection.cursor()
            self.create_database()

    def get_user_by_login(self, login):
        user = self.cursor.execute("SELECT * FROM users WHERE login = '%s'" % login).fetchone()
        return user

    def create_user(self, login, password, firstname, lastname):
        user = self.get_user_by_login(login)
        if user:
            return 'User already exist'
        self.cursor.execute("INSERT INTO users(login,password, firstname, lastname) VALUES ('%s', '%s', '%s', '%s')" %
                            (login, password, firstname, lastname))
        self.connection.commit()

    def get_questions(self):
        db_questions = self.cursor.execute("SELECT * FROM questions order by id").fetchall()
        return db_questions

    def get_next_question(self, q_id):
        question = self.cursor.execute("SELECT * FROM questions where id > %s order by id limit 1" % q_id).fetchall()
        return question[0]

    def get_answer_for_question(self, q_id):
        db_answers = self.cursor.execute("SELECT * FROM answers where question_id=%s" % q_id).fetchall()
        return db_answers

    def get_answer_type_for_question(self, q_id):
        answer_type = self.cursor.execute("SELECT * FROM answer_types where id=%s" % q_id).fetchall()
        return answer_type

    def get_answer_by_data(self, q_id, answer, is_right):
        answer = self.cursor.execute("SELECT * FROM answers where question_id=%s AND answer='%s' AND is_right='%s'" %
                                     (q_id, answer, is_right)).fetchall()
        return answer

    def set_answer(self, q_id, answer, is_right):
        self.cursor.execute("INSERT INTO answers(question_id, answer, is_right) VALUES (%s, '%s', '%s')" %
                            (q_id, answer, is_right))
        return self.get_answer_by_data(q_id, answer, is_right)

    def set_test_result(self, user_id, date, score):
        self.cursor.execute("INSERT INTO test_results(user_id, date, score) VALUES (%s, '%s', '%s')" %
                            (user_id, date, score))
        self.connection.commit()

    def get_test_results(self, user_id):
        test_result = self.cursor.execute("SELECT * FROM test_results where user_id=%s" % user_id).fetchall()
        return test_result

    def _create_tables(self, schema=None):
        if schema is None:
            schema = database
        for table in schema.keys():
            query = "CREATE TABLE %s (" % table
            for column in schema.get(table):
                query += column[0] + " " + column[1] + ", "
            self.cursor.execute(query[:-2] + ");")
        self.connection.commit()

    def _insert_questions(self, questions_list=None):
        if questions_list is None:
            questions_list = questions
        for question in questions_list:
            query = "INSERT INTO questions VALUES (%s, %s, %s)" % (question[0], question[1], question[2])
            self.cursor.execute(query)
        self.connection.commit()

    def _insert_answers(self, answers_list=None):
        if answers_list is None:
            answers_list = answers
        for answer in answers_list:
            query = "INSERT INTO answers(question_id, answer, is_right) VALUES (%s, %s, %s)" % (
                answer[0], answer[1], answer[2])
            self.cursor.execute(query)
        self.connection.commit()

    def _insert_answer_types(self):
        for answer_type in answer_types:
            query = "INSERT INTO answer_types VALUES (%s, %s)" % (answer_type[0], answer_type[1])
            self.cursor.execute(query)
        self.connection.commit()

    def create_database(self, schema=None, questions_list=None, answers_list=None):
        self._create_tables(schema)
        self._insert_questions(questions_list)
        self._insert_answers(answers_list)
        self._insert_answer_types()
