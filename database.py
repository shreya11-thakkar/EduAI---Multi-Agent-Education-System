import sqlite3

DB_NAME = "education_ai.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT UNIQUE,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_note(topic, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO notes (topic, content)
        VALUES (?, ?)
    """, (topic, content))

    conn.commit()
    conn.close()

def get_note(topic):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT content FROM notes WHERE topic = ?
    """, (topic,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return None

def get_all_topics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT topic FROM notes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows] 
