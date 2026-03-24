import subprocess

def encrypt_aes(input_file, output_file, key):
    subprocess.run([
        "openssl", "enc", "-aes-256-cbc",
        "-in", input_file,
        "-out", output_file,
        "-k", key
    ])

def decrypt_aes(input_file, output_file, key):
    subprocess.run([
        "openssl", "enc", "-d", "-aes-256-cbc",
        "-in", input_file,
        "-out", output_file,
        "-k", key
    ])
