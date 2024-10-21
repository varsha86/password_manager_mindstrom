import os
import sqlite3
import hashlib
import time
import pyotp
from cryptography.fernet import Fernet
import shutil
import base64


# Encryption/Decryption Functions
def generate_key(secret):
    return hashlib.sha256(secret.encode()).digest()


def encrypt_data(key, data):
    fernet_key = Fernet(base64.urlsafe_b64encode(key[:32]))
    return fernet_key.encrypt(data.encode())


def decrypt_data(key, encrypted_data):
    fernet_key = Fernet(base64.urlsafe_b64encode(key[:32]))
    return fernet_key.decrypt(encrypted_data).decode()


# Database Functions
def create_table():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords 
                 (website TEXT, username TEXT, password BLOB, timestamp TEXT)''')
    conn.commit()
    conn.close()


def add_password(key):
    website = input("Enter the website: ")
    username = input("Enter the username: ")
    generate = input("Would you like to generate a strong password? (y/n): ")

    if generate.lower() == 'y':
        password = generate_strong_password()
        print(f"Generated password: {password}")
    else:
        password = input("Enter the password: ")

    encrypted_password = encrypt_data(key, password)
    timestamp = time.ctime()

    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute("INSERT INTO passwords (website, username, password, timestamp) VALUES (?, ?, ?, ?)",
              (website, username, encrypted_password, timestamp))
    conn.commit()
    conn.close()


def get_passwords(key):
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute("SELECT website, username, password, timestamp FROM passwords")
    data = c.fetchall()
    conn.close()

    decrypted_data = []
    for (website, username, password, timestamp) in data:
        try:
            decrypted_password = decrypt_data(key, password)
            decrypted_data.append((website, username, decrypted_password, timestamp))
        except Exception as e:
            print(f"Error decrypting password for {website}: {e}")
    
    return decrypted_data


def delete_password(key):
    website = input("Enter the website to delete: ")

    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute("DELETE FROM passwords WHERE website = ?", (website,))
    conn.commit()
    conn.close()

    print(f"Deleted password for {website}")


def search_passwords(key):
    search_query = input("Enter the website or username to search: ")
    
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute("SELECT website, username, password, timestamp FROM passwords WHERE website LIKE ? OR username LIKE ?", 
              ('%' + search_query + '%', '%' + search_query + '%'))
    data = c.fetchall()
    conn.close()

    decrypted_data = []
    for (website, username, password, timestamp) in data:
        try:
            decrypted_password = decrypt_data(key, password)
            decrypted_data.append((website, username, decrypted_password, timestamp))
        except Exception as e:
            print(f"Error decrypting password for {website}: {e}")

    return decrypted_data


def backup_database():
    backup_file = 'password_manager_backup.db'
    shutil.copyfile('password_manager.db', backup_file)
    print(f"Database backed up to {backup_file}")


def restore_database():
    backup_file = 'password_manager_backup.db'
    if os.path.exists(backup_file):
        shutil.copyfile(backup_file, 'password_manager.db')
        print("Database restored from backup.")
    else:
        print("Backup file not found.")


# Helper Functions
def generate_strong_password():
    import random
    import string
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(16))
    return password


def get_totp_token(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()


def check_password_expiry(timestamp):
    password_time = time.strptime(timestamp, "%a %b %d %H:%M:%S %Y")
    current_time = time.localtime()

    time_diff = time.mktime(current_time) - time.mktime(password_time)
    days_passed = time_diff / (24 * 3600)

    if days_passed >= 90:
        print(f"Warning: Password added on {timestamp} has expired. Consider updating it.")


# Main Application Logic
def main():
    secret = pyotp.random_base32()
    print("Your OTP secret is:", secret)
    current_time = time.ctime()
    print("Current system time:", current_time)
    otp = get_totp_token(secret)
    print("Your OTP is:", otp)
    
    entered_otp = input("Enter the OTP: ")
    if entered_otp != otp:
        print("Access Denied")
        return

    # Generate key from secret
    key = hashlib.sha256(secret.encode()).digest()

    # Handle corrupted database by deleting it
    if os.path.exists('password_manager.db'):
        try:
            conn = sqlite3.connect('password_manager.db')
            conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            conn.close()
        except sqlite3.DatabaseError:
            print("Database file is corrupted. Deleting it and creating a new one...")
            conn.close()  # Ensure the connection is closed before deletion
            os.remove('password_manager.db')

    # Call create_table to ensure correct table structure
    create_table()

    while True:
        print("\n1. Add New Password")
        print("2. View Stored Passwords")
        print("3. Delete Password")
        print("4. Search Passwords")
        print("5. Backup Database")
        print("6. Restore Database")
        print("7. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_password(key)
        elif choice == '2':
            passwords = get_passwords(key)
            if passwords:
                for website, username, password, timestamp in passwords:
                    print(f"Website: {website}, Username: {username}, Password: {password}, Added on: {timestamp}")
                    check_password_expiry(timestamp)
            else:
                print("No passwords stored yet.")
        elif choice == '3':
            delete_password(key)
        elif choice == '4':
            results = search_passwords(key)
            if results:
                for website, username, password, timestamp in results:
                    print(f"Website: {website}, Username: {username}, Password: {password}, Added on: {timestamp}")
            else:
                print("No matching records found.")
        elif choice == '5':
            backup_database()
        elif choice == '6':
            restore_database()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
