"""Test comparativ între OpenSSL și PyCryptodome"""
import os
from datetime import datetime

from database.db import initialize_db
from database.crud import *
from crypto.openssl_wrapper import encrypt_aes, decrypt_aes
from crypto.pycryptodome_wrapper import encrypt_aes_pycryptodome, decrypt_aes_pycryptodome
from utils.hashing import calculate_file_hash
from utils.performance import measure_performance


def test_frameworks():
    print("=== Test Comparativ Framework-uri ===\n")
    
    initialize_db()
    
    # Creează fișier de test
    test_file = "test_crypto.txt"
    with open(test_file, "w") as f:
        f.write("Acesta este un test de criptare!" * 100)
    
    key = "parola_secreta_123"
    
    print(f"Fișier test: {test_file}")
    print(f"Dimensiune: {os.path.getsize(test_file)} bytes")
    print(f"Hash original: {calculate_file_hash(test_file)[:16]}...\n")
    
    # Test OpenSSL
    print("--- Test OpenSSL AES-256 ---")
    output_openssl = test_file + ".openssl.enc"
    perf_openssl = measure_performance(encrypt_aes, test_file, output_openssl, key, 256)
    print(f"Timp criptare: {perf_openssl['time']} sec")
    print(f"Memorie: {perf_openssl['memory']} MB")
    print(f"Hash criptat: {calculate_file_hash(output_openssl)[:16]}...")
    
    # Decriptare OpenSSL
    output_openssl_dec = test_file + ".openssl.dec"
    perf_openssl_dec = measure_performance(decrypt_aes, output_openssl, output_openssl_dec, key, 256)
    print(f"Timp decriptare: {perf_openssl_dec['time']} sec")
    print(f"Hash decriptat: {calculate_file_hash(output_openssl_dec)[:16]}...\n")
    
    # Test PyCryptodome
    print("--- Test PyCryptodome AES-256 ---")
    output_pycrypto = test_file + ".pycrypto.enc"
    perf_pycrypto = measure_performance(encrypt_aes_pycryptodome, test_file, output_pycrypto, key)
    print(f"Timp criptare: {perf_pycrypto['time']} sec")
    print(f"Memorie: {perf_pycrypto['memory']} MB")
    print(f"Hash criptat: {calculate_file_hash(output_pycrypto)[:16]}...")
    
    # Decriptare PyCryptodome
    output_pycrypto_dec = test_file + ".pycrypto.dec"
    perf_pycrypto_dec = measure_performance(decrypt_aes_pycryptodome, output_pycrypto, output_pycrypto_dec, key)
    print(f"Timp decriptare: {perf_pycrypto_dec['time']} sec")
    print(f"Hash decriptat: {calculate_file_hash(output_pycrypto_dec)[:16]}...\n")
    
    # Comparație
    print("=== COMPARAȚIE ===")
    print(f"OpenSSL - Criptare: {perf_openssl['time']} sec")
    print(f"PyCryptodome - Criptare: {perf_pycrypto['time']} sec")
    
    faster = "OpenSSL" if perf_openssl['time'] < perf_pycrypto['time'] else "PyCryptodome"
    print(f"\n✓ Mai rapid: {faster}")
    
    # Cleanup
    for f in [test_file, output_openssl, output_openssl_dec, output_pycrypto, output_pycrypto_dec]:
        if os.path.exists(f):
            os.remove(f)
    
    print("\nTest finalizat!")


if __name__ == "__main__":
    test_frameworks()
