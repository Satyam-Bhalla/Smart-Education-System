import sqlite3

def Connection():
    conn = sqlite3.connect('smartes.db')
    c = conn.cursor()
    return c,conn
