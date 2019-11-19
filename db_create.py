import sqlite3

DB_FILE = 'db.db'

database = {
    'users':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('login', 'TEXT NOT NULL'),
            ('password', 'TEXT')
        ],
    'questions':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('question', 'TEXT NOT NULL')
        ],
    'answers':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('question_id', 'INTEGER NOT NULL'),
            ('answer', 'TEXT NOT NULL'),
            ('is_right', 'NUMERIC NOT NULL DEFAULT FALSE'),
            ('', 'FOREIGN KEY(question_id) REFERENCES questions(id)')
        ],
    'tests':
        [
            ('id', 'INTEGER PRIMARY KEY NOT NULL'),
            ('user_id', 'INTEGER NOT NULL'),
            ('date', 'NUMERIC'),
            ('score', 'INTEGER DEFAULT 0'),
            ('', 'FOREIGN KEY(user_id) REFERENCES users(id)')
        ]
}

questions = [('1', '"Какое из утверждений верно?"'),
             ('2', '"Какие из утверждений не верны?"'),
             ('3', '"Сколько часов в сутках?"')
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


def create_tables(cur):
    for table in database.keys():
        query = "CREATE TABLE %s (" % table
        for column in database.get(table):
            query += column[0] + " " + column[1] + ", "
        cur.execute(query[:-2] + ");")
    connection.commit()


def insert_questions(cur):
    for question in questions:
        query = "INSERT INTO questions VALUES (%s, %s)" % (question[0], question[1])
        cur.execute(query)
    connection.commit()


def insert_answers(cur):
    for answer in answers:
        query = "INSERT INTO answers(question_id, answer, is_right) VALUES (%s, %s, %s)" % (
            answer[0], answer[1], answer[2])
        cur.execute(query)
    connection.commit()


def create_database(cur):
    create_tables(cur)
    insert_questions(cur)
    insert_answers(cur)


if __name__ == '__main__':
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    create_database(cursor)
    connection.close()
