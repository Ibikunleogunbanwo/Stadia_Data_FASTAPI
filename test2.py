import sqlite3

DB_PATH = "stadiums.db"

def show_stadium():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stadia")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

print(show_stadium())