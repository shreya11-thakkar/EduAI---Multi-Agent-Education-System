import sqlite3

conn = sqlite3.connect("education_ai.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM notes")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
