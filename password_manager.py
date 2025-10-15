import sqlite3
import random
import string
from cryptography.fernet import Fernet

# Generate encryption key (run once to create and save)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load encryption key
def load_key():
    return open("secret.key", "rb").read()

# Initialize database
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Generate strong random password
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# Save credentials securely
def save_password(website, username, password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                   (website, username, encrypted_password))
    conn.commit()
    conn.close()

# Retrieve password
def get_password(website):
    key = load_key()
    f = Fernet(key)

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE website=?", (website,))
    record = cursor.fetchone()
    conn.close()

    if record:
        username, encrypted_password = record
        decrypted_password = f.decrypt(encrypted_password).decode()
        return username, decrypted_password
    else:
        return None, None
