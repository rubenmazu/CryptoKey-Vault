import sqlite3

DB_PATH = "database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


# FILE CRUD

def insert_file(name, path, size, status='original'):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO File (name, path, size, status) VALUES (?, ?, ?, ?)",
        (name, path, size, status)
    )
    conn.commit()
    conn.close()


def get_file_by_id(file_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM File WHERE id = ?", (file_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_file_name(file_id, new_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE File SET name = ? WHERE id = ?",
        (new_name, file_id)
    )
    conn.commit()
    conn.close()


def delete_file(file_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM File WHERE id = ?", (file_id,))
    conn.commit()
    conn.close()


# ALGORITHM CRUD

def insert_algorithm(name, type, key_size, framework, is_asymmetric=0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Algorithm (name, type, key_size, framework, is_asymmetric)
        VALUES (?, ?, ?, ?, ?)
    """, (name, type, key_size, framework, is_asymmetric))
    conn.commit()
    conn.close()


def get_algorithm_by_id(algorithm_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Algorithm WHERE id = ?", (algorithm_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_algorithm_name(algorithm_id, new_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Algorithm SET name = ? WHERE id = ?",
        (new_name, algorithm_id)
    )
    conn.commit()
    conn.close()


def delete_algorithm(algorithm_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Algorithm WHERE id = ?", (algorithm_id,))
    conn.commit()
    conn.close()


def get_algorithms():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Algorithm")
    rows = cur.fetchall()
    conn.close()
    return rows


# KEY CRUD

def insert_key(algorithm_id, value, date_generated):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO KeyTable (algorithm_id, value, date_generated)
        VALUES (?, ?, ?)
    """, (algorithm_id, value, date_generated))
    conn.commit()
    conn.close()


def get_key_by_id(key_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM KeyTable WHERE id = ?", (key_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_key_value(key_id, new_value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE KeyTable SET value = ? WHERE id = ?",
        (new_value, key_id)
    )
    conn.commit()
    conn.close()


def delete_key(key_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM KeyTable WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()


# OPERATION CRUD

def insert_operation(file_id, key_id, algorithm_id, op_type, framework, time, memory, file_hash, date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Operation (file_id, key_id, algorithm_id, op_type, framework, time, memory, file_hash, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (file_id, key_id, algorithm_id, op_type, framework, time, memory, file_hash, date))
    conn.commit()
    conn.close()


def get_operation_by_id(operation_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Operation WHERE id = ?", (operation_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_operation_time(operation_id, new_time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Operation SET time = ? WHERE id = ?",
        (new_time, operation_id)
    )
    conn.commit()
    conn.close()


def delete_operation(operation_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Operation WHERE id = ?", (operation_id,))
    conn.commit()
    conn.close()


def update_file_status(file_id, status):
    """Actualizează statusul fișierului (original/encrypted/decrypted)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE File SET status = ? WHERE id = ?",
        (status, file_id)
    )
    conn.commit()
    conn.close()
