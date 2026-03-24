import sqlite3

def get_connection():
    return sqlite3.connect("database.db")

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabel Algorithm
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Algorithm (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        key_size INTEGER,
        framework TEXT NOT NULL
    )
    """)

    # Tabel Key
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS KeyTable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        algorithm_id INTEGER NOT NULL,
        value TEXT NOT NULL,
        date_generated TEXT NOT NULL,
        FOREIGN KEY (algorithm_id) REFERENCES Algorithm(id)
    )
    """)

    # Tabel File
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS File (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        size INTEGER NOT NULL
    )
    """)

    # Tabel Operation
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Operation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        key_id INTEGER NOT NULL,
        algorithm_id INTEGER NOT NULL,
        op_type TEXT NOT NULL,
        framework TEXT NOT NULL,
        time REAL,
        memory INTEGER,
        file_hash TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY (file_id) REFERENCES File(id),
        FOREIGN KEY (key_id) REFERENCES KeyTable(id),
        FOREIGN KEY (algorithm_id) REFERENCES Algorithm(id)
    )
    """)

    conn.commit()
    conn.close()