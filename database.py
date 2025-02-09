import aiosqlite
from datetime import datetime

DB_NAME = "quiz.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                avatar_url TEXT,
                age INTEGER,
                language TEXT,
                created_at DATETIME NOT NULL
            )
        """)
        await db.commit()

async def save_user_data(
    user_id: int,
    username: str,
    avatar_url: str,
    age: int,
    language: str
):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO users 
            (user_id, username, avatar_url, age, language, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, avatar_url, age, language, datetime.now()))
        await db.commit()