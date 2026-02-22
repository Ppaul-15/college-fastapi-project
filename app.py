from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database location
DATABASE = os.path.join(os.path.dirname(__file__), "users.db")

# Create table
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            designation TEXT,
            location TEXT,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


@app.post("/login")
async def login(data: dict):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, age, designation, location, email)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("name"),
        data.get("age"),
        data.get("designation"),
        data.get("location"),
        data.get("email")
    ))

    conn.commit()
    conn.close()

    return {"success": True}
    @app.get("/users")
def get_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    conn.close()

    return {"data": rows}
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
