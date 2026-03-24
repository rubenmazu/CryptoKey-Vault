import subprocess

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
