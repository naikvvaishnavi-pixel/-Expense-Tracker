import sqlite3
try:

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    print("Database connected successfully")
except Exception as e:
    print("Database connection failed:",e)

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    Name TEXT NOT NULL,
    Username TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit()
