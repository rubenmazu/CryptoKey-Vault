from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

def encrypt_aes_pycryptodome(input_file, output_file, key):
    """Criptare AES folosind PyCryptodome"""
    # Asigură că cheia are 32 bytes (256 bits)
    key_bytes = key.encode('utf-8')[:32].ljust(32, b'\0')
    
    cipher = AES.new(key_bytes, AES.MODE_CBC)
    
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    
    with open(output_file, 'wb') as f:
        f.write(cipher.iv)
        f.write(ciphertext)


def decrypt_aes_pycryptodome(input_file, output_file, key):
    """Decriptare AES folosind PyCryptodome"""
    key_bytes = key.encode('utf-8')[:32].ljust(32, b'\0')
    
    with open(input_file, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    with open(output_file, 'wb') as f:
        f.write(plaintext)
