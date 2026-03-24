import os
from datetime import datetime

from database.db import initialize_db, get_connection
from database.crud import (
    insert_file,
    insert_key,
    insert_operation,
    insert_algorithm,
    get_algorithms,
    get_algorithm_by_id)

from crypto.openssl_wrapper import encrypt_aes, decrypt_aes


DB_PATH = "database.db"


def setup_default_algorithms():
    algorithms = get_algorithms()

    if len(algorithms) == 0:
        insert_algorithm("AES-128", "symmetric", 128, "OpenSSL")
        insert_algorithm("AES-256", "symmetric", 256, "OpenSSL")
        print("Algoritmii default au fost adaugati.")
    else:
        print("Algoritmii exista deja.")


def select_file():
    path = input("\nIntrodu calea fisierului: ")

    if not os.path.exists(path):
        print("Fisierul nu exista.")
        return None, None

    name = os.path.basename(path)
    size = os.path.getsize(path)

    insert_file(name, path, size)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM File WHERE path = ?", (path,))
    file_id = cur.fetchone()[0]
    conn.close()

    print(f"Fisierul '{name}' a fost inregistrat in DB.")
    return path, file_id


def select_or_generate_key(algorithm_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM KeyTable WHERE algorithm_id = ?", (algorithm_id,))
    keys = cur.fetchall()

    print("\nSelecteaza cheia:")
    for key in keys:
        print(f"{key[0]}. {key[2][:20]}... (generata la {key[3]})")

    print("0. Genereaza cheie noua")

    while True:
        try:
            choice = int(input("Alege: "))
            break
        except ValueError:
            print("Introdu un numar valid.")

    if choice == 0:
        new_key = input("Introdu valoarea cheii: ")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_key(algorithm_id, new_key, date)

        cur.execute("SELECT id FROM KeyTable ORDER BY id DESC LIMIT 1")
        key_id = cur.fetchone()[0]

        conn.close()
        return new_key, key_id

    else:
        for key in keys:
            if key[0] == choice:
                conn.close()
                return key[2], key[0]

        print("ID invalid. Reincearca.")
        conn.close()
        return select_or_generate_key(algorithm_id)


def select_algorithm():
    algorithms = get_algorithms()

    print("\nAlege algoritmul de criptare:\n")

    for alg in algorithms:
        print(f"{alg[0]}. {alg[1]}  |  Tip: {alg[2]}  |  Cheie: {alg[3]} bits  |  Framework: {alg[4]}")

    while True:
        try:
            choice = int(input("\nIntrodu ID-ul algoritmului: "))
            ids = [alg[0] for alg in algorithms]
            if choice in ids:
                return choice
            else:
                print("ID invalid. Alege un ID din lista.")
        except ValueError:
            print("Introdu un numar valid.")


def run_encryption_flow():
    alg_id = select_algorithm()
    algorithm = get_algorithm_by_id(alg_id)
    key_size = algorithm[3]   
    key, key_id = select_or_generate_key(alg_id)
    file_path, file_id = select_file()

    print("\nAlege operatia:")
    print("1. Criptare")
    print("2. Decriptare")

    while True:
        try:
            op = int(input("Alege: "))
            if op in (1, 2):
                break
            print("Alege 1 sau 2.")
        except ValueError:
            print("Introdu un numar valid.")

    output = file_path + (".enc" if op == 1 else ".dec")

    if op == 1:
        encrypt_aes(file_path, output, key, key_size)
        op_type = "encrypt"
    else:
        decrypt_aes(file_path, output, key, key_size)
        op_type = "decrypt"

    insert_operation(
        file_id,
        key_id,
        alg_id,
        op_type,
        "OpenSSL",
        None,
        None,
        None,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    print(f"\nOperatia '{op_type}' a fost salvata in DB.")
    print(f"Fisier rezultat: {output}")


def main():
    print("Encryption Manager")
    initialize_db()
    setup_default_algorithms()
    run_encryption_flow()


if __name__ == "__main__":
    main()
