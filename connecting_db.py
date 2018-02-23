import sqlite3

def Connection():
    conn = sqlite3.connect('question_answers_db.db')
    c = conn.cursor()
    return c,conn
