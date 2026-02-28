import sqlite3

conn = sqlite3.connect("memory.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    summary TEXT,
    reply TEXT
)
""")

conn.commit()

def store_email(content, summary, reply):
    c.execute(
        "INSERT INTO emails (content, summary, reply) VALUES (?, ?, ?)",
        (content, summary, reply)
    )
    conn.commit()
