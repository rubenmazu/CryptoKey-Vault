import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os

from database.db import initialize_db
from database.crud import *
from crypto.openssl_wrapper import encrypt_aes, decrypt_aes
from crypto.pycryptodome_wrapper import encrypt_aes_pycryptodome, decrypt_aes_pycryptodome
from utils.hashing import calculate_file_hash
from utils.performance import measure_performance


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoKey-Vault")
        self.root.geometry("700x600")
        
        initialize_db()
        self.setup_default_algorithms()
        
        self.create_widgets()
    
    def setup_default_algorithms(self):
        algorithms = get_algorithms()
        if len(algorithms) == 0:
            insert_algorithm("AES-128", "symmetric", 128, "OpenSSL")
            insert_algorithm("AES-256", "symmetric", 256, "OpenSSL")
            insert_algorithm("AES-256", "symmetric", 256, "PyCryptodome")
    
    def create_widgets(self):
        # Frame pentru selectare fișier
        file_frame = ttk.LabelFrame(self.root, text="Fișier", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="Niciun fișier selectat")
        self.file_label.pack(side="left", padx=5)
        
        ttk.Button(file_frame, text="Selectează Fișier", command=self.select_file).pack(side="right")
        
        # Frame pentru algoritm
        algo_frame = ttk.LabelFrame(self.root, text="Algoritm", padding=10)
        algo_frame.pack(fill="x", padx=10, pady=5)
        
        self.algo_var = tk.StringVar()
        algorithms = get_algorithms()
        algo_list = [f"{a[0]}: {a[1]} ({a[4]})" for a in algorithms]
        self.algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=algo_list, state="readonly", width=40)
        if algo_list:
            self.algo_combo.current(0)
        self.algo_combo.pack()
        
        # Frame pentru cheie
        key_frame = ttk.LabelFrame(self.root, text="Cheie", padding=10)
        key_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(key_frame, text="Introdu cheia:").pack()
        self.key_entry = ttk.Entry(key_frame, width=50, show="*")
        self.key_entry.pack(pady=5)
        
        self.show_key_var = tk.BooleanVar()
        ttk.Checkbutton(key_frame, text="Arată cheia", variable=self.show_key_var, 
                       command=self.toggle_key_visibility).pack()
        
        # Frame pentru operații
        op_frame = ttk.LabelFrame(self.root, text="Operație", padding=10)
        op_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(op_frame, text="Criptează", command=self.encrypt_file, width=20).pack(side="left", padx=5)
        ttk.Button(op_frame, text="Decriptează", command=self.decrypt_file, width=20).pack(side="left", padx=5)
        
        # Frame pentru rezultate
        result_frame = ttk.LabelFrame(self.root, text="Rezultate", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(result_frame, height=15, width=70)
        self.result_text.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)
    
    def toggle_key_visibility(self):
        if self.show_key_var.get():
            self.key_entry.config(show="")
        else:
            self.key_entry.config(show="*")
    
    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
    
    def log(self, message):
        self.result_text.insert("end", message + "\n")
        self.result_text.see("end")
        self.root.update()
    
    def encrypt_file(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Eroare", "Selectează un fișier!")
            return
        
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Eroare", "Introdu o cheie!")
            return
        
        self.result_text.delete(1.0, "end")
        self.log("=== Începe criptarea ===")
        
        # Obține algoritmul
        algo_id = int(self.algo_var.get().split(":")[0])
        algorithm = get_algorithm_by_id(algo_id)
        
        # Calculează hash înainte
        hash_before = calculate_file_hash(self.selected_file)
        self.log(f"Hash original: {hash_before[:16]}...")
        
        # Înregistrează fișierul
        name = os.path.basename(self.selected_file)
        size = os.path.getsize(self.selected_file)
        insert_file(name, self.selected_file, size, 'original')
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM File ORDER BY id DESC LIMIT 1")
        file_id = cur.fetchone()[0]
        conn.close()
        
        # Înregistrează cheia
        insert_key(algo_id, key, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM KeyTable ORDER BY id DESC LIMIT 1")
        key_id = cur.fetchone()[0]
        conn.close()
        
        output = self.selected_file + ".enc"
        
        # Criptează cu măsurare performanță
        framework = algorithm[4]
        if framework == "OpenSSL":
            perf = measure_performance(encrypt_aes, self.selected_file, output, key, algorithm[3])
        else:
            perf = measure_performance(encrypt_aes_pycryptodome, self.selected_file, output, key)
        
        self.log(f"Framework: {framework}")
        self.log(f"Timp: {perf['time']} secunde")
        self.log(f"Memorie: {perf['memory']} MB")
        
        # Calculează hash după
        hash_after = calculate_file_hash(output)
        self.log(f"Hash criptat: {hash_after[:16]}...")
        
        # Salvează operația
        insert_operation(file_id, key_id, algo_id, "encrypt", framework, 
                        perf['time'], perf['memory'], hash_after, 
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        self.log(f"\n✓ Fișier criptat: {output}")
        messagebox.showinfo("Succes", "Fișier criptat cu succes!")
    
    def decrypt_file(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Eroare", "Selectează un fișier!")
            return
        
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Eroare", "Introdu o cheie!")
            return
        
        self.result_text.delete(1.0, "end")
        self.log("=== Începe decriptarea ===")
        
        algo_id = int(self.algo_var.get().split(":")[0])
        algorithm = get_algorithm_by_id(algo_id)
        
        output = self.selected_file.replace(".enc", ".dec")
        
        framework = algorithm[4]
        if framework == "OpenSSL":
            perf = measure_performance(decrypt_aes, self.selected_file, output, key, algorithm[3])
        else:
            perf = measure_performance(decrypt_aes_pycryptodome, self.selected_file, output, key)
        
        self.log(f"Framework: {framework}")
        self.log(f"Timp: {perf['time']} secunde")
        self.log(f"Memorie: {perf['memory']} MB")
        
        hash_decrypted = calculate_file_hash(output)
        self.log(f"Hash decriptat: {hash_decrypted[:16]}...")
        
        self.log(f"\n✓ Fișier decriptat: {output}")
        messagebox.showinfo("Succes", "Fișier decriptat cu succes!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
