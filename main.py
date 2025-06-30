import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

class Stadium(BaseModel):
    id: int | None = None
    name: str
    city: str
    capacity: int
    club: str | None = None
    open_year: int

app = FastAPI(title="Stadium Directory")

DB_PATH = "stadiums.db"

@app.on_event("startup")
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stadia(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE, 
            city TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            club TEXT,
            open_year INTEGER NOT NULL
        )

        """
    )
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@app.post("/create_stadium/", response_model=Stadium, status_code=201)
def add_stadium(stadium: Stadium, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO stadia(name, city, capacity, club, open_year)
            VALUES (?, ?, ?, ?,?)
            """,
            (stadium.name, stadium.city, stadium.capacity,stadium.club,stadium.open_year)
        )
        db.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(400, detail="Stadium with thesame name alrady exists")
    stadium.id = cursor.lastrowid
    return stadium



@app.get('/stadiums/', response_model=List[Stadium])
def list_stadiums(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM stadia")
    rows = cursor.fetchall()
    return [Stadium(**row) for row in rows]



@app.get("/stadium/{stadium_id}", response_model=Stadium)
def get_stadium_by_id(stadium_id: int,db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM stadia WHERE id = ?", (stadium_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(404, detail="Stadium not found")
    return Stadium(**row)



@app.get("/stadium_name/{stadium_name}", response_model=Stadium)
def get_stadium_by_name(stadium_name: str,db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM stadia WHERE lower(name) = ?", (stadium_name.lower(),))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(404, detail="Stadium not found")
    return Stadium(**row)



@app.put("/stadium_by_id/{stadium_id}", response_model=Stadium)
def update_stadium(stadium_id: int, data: Stadium, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute ("select * from stadia where id = ?", (stadium_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="stadium not found")
    
    cursor.execute("""
                    UPDATE stadia
                    SET name = ?, city = ?, club = ?, capacity = ?, open_year = ?
                    where id =?
                    """,
                    (data.name, data.city, data.club, data.capacity, data.open_year, data.id)

                    )
    db.commit()
    data.id = stadium_id
    return data

@app.delete("/stadium/{stadium_id}", status_code=204)
def delete_stadium (stadium_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("select id from stadia where id =?", (stadium_id,))
    if not cursor.fetchone():
        return HTTPException(status_code=400, detail="stadium not found")
    
    cursor.execute("delete from stadia where id = ?", (stadium_id,))
    db.commit()
    return

    