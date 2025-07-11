# app/db.py

import sqlite3

DB_FILE = \"labels.db\"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS images (
            image_id TEXT PRIMARY KEY,
            image_path TEXT,
            labels TEXT,
            description TEXT
        )
    \"\"\")
    conn.commit()
    conn.close()

def insert_label(image_id, image_path, labels, description):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(\"INSERT INTO images VALUES (?, ?, ?, ?)\",
                   (image_id, image_path, \",\".join(labels), description))
    conn.commit()
    conn.close()

def get_label(image_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(\"SELECT * FROM images WHERE image_id = ?\", (image_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_all_labels():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(\"SELECT * FROM images\")
    rows = cursor.fetchall()
    conn.close()
    return rows
