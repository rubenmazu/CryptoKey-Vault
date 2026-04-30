import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os

from database.db import initialize_db
from database.crud import *
from crypto.openssl_wrapper import encrypt_aes, decrypt_aes, generate_rsa_keys, encrypt_rsa_public, decrypt_rsa_private
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
            insert_algorithm("AES-128", "symmetric", 128, "OpenSSL", 0)
            insert_algorithm("AES-256", "symmetric", 256, "OpenSSL", 0)
            insert_algorithm("AES-256", "symmetric", 256, "PyCryptodome", 0)
            insert_algorithm("RSA-2048", "asymmetric", 2048, "OpenSSL", 1)
            insert_algorithm("RSA-4096", "asymmetric", 4096, "OpenSSL", 1)
    
    def create_widgets(self):
        # Frame pentru selectare fisier
        file_frame = ttk.LabelFrame(self.root, text="Fisier", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="Niciun fisier selectat")
        self.file_label.pack(side="left", padx=5)
        
        ttk.Button(file_frame, text="Selecteaza Fisier", command=self.select_file).pack(side="right")
        
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
        
        ttk.Label(key_frame, text="Introdu cheia (sau genereaza RSA):").pack()
        self.key_entry = ttk.Entry(key_frame, width=50, show="*")
        self.key_entry.pack(pady=5)
        
        key_buttons = ttk.Frame(key_frame)
        key_buttons.pack()
        
        self.show_key_var = tk.BooleanVar()
        ttk.Checkbutton(key_buttons, text="Arata cheia", variable=self.show_key_var, 
                       command=self.toggle_key_visibility).pack(side="left", padx=5)
        
        ttk.Button(key_buttons, text="Genereaza Chei RSA", command=self.generate_rsa).pack(side="left", padx=5)
        
        # Frame pentru operatii
        op_frame = ttk.LabelFrame(self.root, text="Operatie", padding=10)
        op_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(op_frame, text="Cripteaza", command=self.encrypt_file, width=20).pack(side="left", padx=5)
        ttk.Button(op_frame, text="Decripteaza", command=self.decrypt_file, width=20).pack(side="left", padx=5)
        
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
    
    def generate_rsa(self):
        """Genereaza pereche de chei RSA"""
        algo_id = int(self.algo_var.get().split(":")[0])
        algorithm = get_algorithm_by_id(algo_id)
        
        if algorithm[5] != 1:  # nu e asymmetric
            messagebox.showwarning("Atentie", "Selecteaza un algoritm RSA pentru a genera chei!")
            return
        
        self.log("Generez chei RSA...")
        key_size = algorithm[3]
        
        try:
            private_key, public_key = generate_rsa_keys(key_size)
            self.log(f"✓ Chei generate:")
            self.log(f"  - Cheie privata: {private_key}")
            self.log(f"  - Cheie publica: {public_key}")
            
            # Salveaza calea cheii private in entry
            self.key_entry.delete(0, "end")
            self.key_entry.insert(0, private_key)
            
            messagebox.showinfo("Succes", f"Chei RSA generate!\n\nPrivata: {private_key}\nPublica: {public_key}")
        except Exception as e:
            self.log(f"✗ Eroare: {str(e)}")
            messagebox.showerror("Eroare", f"Nu s-au putut genera cheile: {str(e)}")
    
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
            messagebox.showerror("Eroare", "Selecteaza un fisier!")
            return
        
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Eroare", "Introdu o cheie!")
            return
        
        self.result_text.delete(1.0, "end")
        self.log("=== incepe criptarea ===")
        
        # Obtine algoritmul
        algo_id = int(self.algo_var.get().split(":")[0])
        algorithm = get_algorithm_by_id(algo_id)
        is_rsa = algorithm[5] == 1
        
        # Calculeaza hash inainte
        hash_before = calculate_file_hash(self.selected_file)
        self.log(f"Hash original: {hash_before[:16]}...")
        
        # inregistreaza fisierul
        name = os.path.basename(self.selected_file)
        size = os.path.getsize(self.selected_file)
        insert_file(name, self.selected_file, size, 'original')
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM File ORDER BY id DESC LIMIT 1")
        file_id = cur.fetchone()[0]
        conn.close()
        
        # inregistreaza cheia
        insert_key(algo_id, key, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM KeyTable ORDER BY id DESC LIMIT 1")
        key_id = cur.fetchone()[0]
        conn.close()
        
        output = self.selected_file + ".enc"
        
        # Cripteaza cu masurare performanta
        framework = algorithm[4]
        
        try:
            if is_rsa:
                # Pentru RSA, key e calea catre cheia privata
                # Trebuie sa existe si cheia publica
                public_key = key.replace("private", "public")
                if not os.path.exists(public_key):
                    raise Exception(f"Cheia publica nu exista: {public_key}")
                
                self.log(f"Folosesc cheie publica: {public_key}")
                perf = measure_performance(encrypt_rsa_public, self.selected_file, output, public_key)
            elif framework == "OpenSSL":
                perf = measure_performance(encrypt_aes, self.selected_file, output, key, algorithm[3])
            else:
                perf = measure_performance(encrypt_aes_pycryptodome, self.selected_file, output, key)
            
            self.log(f"Framework: {framework}")
            self.log(f"Algoritm: {algorithm[1]}")
            self.log(f"Timp: {perf['time']} secunde")
            self.log(f"Memorie: {perf['memory']} MB")
            
            # Calculeaza hash dupa
            hash_after = calculate_file_hash(output)
            self.log(f"Hash criptat: {hash_after[:16]}...")
            
            # Salveaza operatia
            insert_operation(file_id, key_id, algo_id, "encrypt", framework, 
                            perf['time'], perf['memory'], hash_after, 
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Actualizeaza statusul fisierului original
            update_file_status(file_id, 'encrypted')
            
            # inregistreaza fisierul criptat in DB
            insert_file(os.path.basename(output), output, os.path.getsize(output), 'encrypted')
            
            self.log(f"\n✓ Fisier criptat: {output}")
            self.log(f"✓ Status actualizat: encrypted")
            messagebox.showinfo("Succes", "Fisier criptat cu succes!")
        except Exception as e:
            self.log(f"\n✗ Eroare: {str(e)}")
            messagebox.showerror("Eroare", f"Criptare esuata: {str(e)}")
    
    def decrypt_file(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Eroare", "Selecteaza un fisier!")
            return
        
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Eroare", "Introdu o cheie!")
            return
        
        self.result_text.delete(1.0, "end")
        self.log("incepe decriptarea")
        
        algo_id = int(self.algo_var.get().split(":")[0])
        algorithm = get_algorithm_by_id(algo_id)
        is_rsa = algorithm[5] == 1
        
        output = self.selected_file.replace(".enc", ".dec")
        
        framework = algorithm[4]
        
        try:
            if is_rsa:
                # Pentru RSA, key e calea catre cheia privata
                if not os.path.exists(key):
                    raise Exception(f"Cheia privata nu exista: {key}")
                
                self.log(f"Folosesc cheie privata: {key}")
                perf = measure_performance(decrypt_rsa_private, self.selected_file, output, key)
            elif framework == "OpenSSL":
                perf = measure_performance(decrypt_aes, self.selected_file, output, key, algorithm[3])
            else:
                perf = measure_performance(decrypt_aes_pycryptodome, self.selected_file, output, key)
            
            self.log(f"Framework: {framework}")
            self.log(f"Algoritm: {algorithm[1]}")
            self.log(f"Timp: {perf['time']} secunde")
            self.log(f"Memorie: {perf['memory']} MB")
            
            hash_decrypted = calculate_file_hash(output)
            self.log(f"Hash decriptat: {hash_decrypted[:16]}...")
            
            # inregistreaza fisierul decriptat in DB
            insert_file(os.path.basename(output), output, os.path.getsize(output), 'decrypted')
            
            self.log(f"\n✓ Fisier decriptat: {output}")
            self.log(f"✓ Status: decrypted")
            messagebox.showinfo("Succes", "Fisier decriptat cu succes!")
        except Exception as e:
            self.log(f"\n✗ Eroare: {str(e)}")
            messagebox.showerror("Eroare", f"Decriptare esuata: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
