import sqlite3
from tabulate import tabulate

def view_database():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    tables = ["Algorithm", "KeyTable", "File", "Operation"]
    
    for table in tables:
        print(f"\n{'='*60}")
        print(f"Tabelul: {table}")
        print('='*60)
        
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        
        if rows:
            # Obține numele coloanelor
            cur.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cur.fetchall()]
            
            # Afișează datele în format tabel
            print(tabulate(rows, headers=columns, tablefmt="grid"))
        else:
            print("(Tabelul este gol)")
    
    conn.close()

if __name__ == "__main__":
    view_database()
