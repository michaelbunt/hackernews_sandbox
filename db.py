#db.py
import sqlite3
import logging
from pathlib import Path

DB_PATH = Path("posts.db")

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    schema = """
    CREATE TABLE IF NOT EXISTS posts (
        id         INTEGER PRIMARY KEY,
        title      TEXT NOT NULL,
        upvotes     INTEGER NOT NULL,
        comments   INTEGER NOT NULL,
        summary    TEXT NOT NULL,
        url        TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    with get_conn() as conn:
        conn.executescript(schema)

def insert_row(post):
    sql = """
    INSERT OR IGNORE INTO posts
    (id, title, upvotes, comments, summary, url)
    VALUES (?, ?, ?, ?, ?, ?);
    """

    values = (
        post["id"],
        post["title"],
        post["upvotes"],
        post["comments"],
        post["summary"],
        post["url"]
    )

    with get_conn() as conn:
        conn.execute(sql, values)
        conn.commit

def fetch_latest(n=10):
    sql = """
    SELECT id, title, upvotes, comments, summary, url, created_at
    FROM posts
    ORDER BY created_at DESC
    LIMIT ?;
    """
    with get_conn() as conn:
        return conn.execute(sql, (n,)).fetchall()