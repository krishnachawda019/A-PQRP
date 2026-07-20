import sqlite3

def connect_db() :
    conn = sqlite3.connect("backend/users.db", check_same_thread = False)
    return conn

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL 
) """)

conn.commit()