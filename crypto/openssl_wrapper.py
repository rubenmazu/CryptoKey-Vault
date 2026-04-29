import subprocess
import os

def encrypt_aes(input_file, output_file, key, key_size):
    algo = f"-aes-{key_size}-cbc"
    subprocess.run([
        "openssl", "enc", algo,
        "-in", input_file,
        "-out", output_file,
        "-k", key
    ])


def decrypt_aes(input_file, output_file, key, key_size):
    algo = f"-aes-{key_size}-cbc"
    subprocess.run([
        "openssl", "enc", "-d", algo,
        "-in", input_file,
        "-out", output_file,
        "-k", key
    ])


def encrypt_rsa_public(input_file, output_file, public_key_file):
    """Criptare RSA cu cheie publică"""
    subprocess.run([
        "openssl", "rsautl", "-encrypt",
        "-inkey", public_key_file,
        "-pubin",
        "-in", input_file,
        "-out", output_file
    ])


def decrypt_rsa_private(input_file, output_file, private_key_file):
    """Decriptare RSA cu cheie privată"""
    subprocess.run([
        "openssl", "rsautl", "-decrypt",
        "-inkey", private_key_file,
        "-in", input_file,
        "-out", output_file
    ])


def generate_rsa_keys(key_size=2048):
    """Generează pereche de chei RSA"""
    private_key = f"rsa_private_{key_size}.pem"
    public_key = f"rsa_public_{key_size}.pem"
    
    # Generează cheia privată
    subprocess.run([
        "openssl", "genrsa",
        "-out", private_key,
        str(key_size)
    ])
    
    # Extrage cheia publică
    subprocess.run([
        "openssl", "rsa",
        "-in", private_key,
        "-pubout",
        "-out", public_key
    ])
    
    return private_key, public_key
