import sqlite3
conn = sqlite3.connect('question_answers_db.db')
c = conn.cursor()
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY,first_name TEXT,last_name TEXT,email TEXT, password TEXT)")
    c.close()
    conn.close()
create_table()
