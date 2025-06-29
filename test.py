import sqlite3
from fastapi import Depends
DB_PATH = "stadiums.db"


def show_staduim():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stadia")
    rows = cursor.fetchall()
    return [ row for row in rows]

print(show_staduim())