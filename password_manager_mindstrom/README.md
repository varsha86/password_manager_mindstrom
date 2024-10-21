Password Manager Application

This is a Python-based password manager application that securely stores and manages user passwords. The application uses strong encryption techniques to protect the password database and provides a feature to access it using multi-factor authentication (MFA). Additional features include password search, backup/restore functionality, and expiration warnings for old passwords.

Features

- Secure Password Storage: Uses AES encryption via the `cryptography` package to securely store passwords.
- Multi-Factor Authentication (MFA): OTP (One-Time Password) is generated using the `pyotp` library for added security.
- Add Password: Users can securely store new passwords for different websites/services.
- View Stored Passwords: Lists all stored passwords, decrypting them on the fly.
- Delete Password: Allows deletion of passwords by specifying the website.
- Search Passwords: Users can search for passwords by website or username.
- Backup Database: Creates a backup of the password database.
- Restore Database: Restores the database from a backup file.
- Password Expiration Warnings: Notifies users when a password has exceeded a predefined age (90 days).
- Strong Password Generator: Automatically generates strong, random passwords for users when adding new credentials.
- Encrypted Database: Data is stored in an encrypted SQLite database to ensure confidentiality and data integrity.

Prerequisites

Before running this application, you need to install the required libraries:

```bash
pip install cryptography pyotp
```

How to Run

1. Clone the Repository
   ```bash
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
   ```

2. Run the Application
   ```bash
   python password_manager.py
   ```

3. OTP Authentication
   - On launching the app, an OTP secret will be generated.
   - An OTP (One-Time Password) will be generated based on the system time and secret.
   - Enter the OTP to authenticate and access the password manager.

Database Structure

The password data is stored in a local SQLite database file (`password_manager.db`). The database consists of the following fields:

- `website`: The website or service for which the password is stored.
- `username`: The username associated with the website/service.
- `password`: The encrypted password.
- `timestamp`: The time when the password was added, used for checking expiration.

Example Workflow

1. OTP Verification:  
   The user is required to enter a one-time password (OTP) for secure access to the manager.
   
2. Adding a New Password:  
   When adding a password, the user can either input their own password or let the app generate a strong password. The password is encrypted before being stored in the SQLite database.

3. Viewing Stored Passwords:  
   The application will display all saved passwords in decrypted form. It also checks the timestamp of when the password was created and warns users if the password is older than 90 days.

4. Deleting Passwords:  
   Users can delete a password entry by specifying the associated website.

5. Backup & Restore:  
   Users can create a backup of the database or restore it from a previously saved backup.

Error Handling

- Corrupted Database: If the database file is corrupted, the program will delete the corrupted file and create a new one.
- Password Decryption Errors: Any errors during password decryption will be handled and reported to the user without crashing the application.

Code Structure

- `encrypt_data()`: Encrypts the password using the encryption key.
- `decrypt_data()`: Decrypts the stored passwords.
- `generate_strong_password()`: Generates a random, strong password.
- `add_password()`: Prompts the user to add a new password entry.
- `get_passwords()`: Retrieves all stored passwords and decrypts them.
- `delete_password()`: Allows the user to delete a stored password.
- `search_passwords()`: Searches passwords by website or username.
- `backup_database()`: Creates a backup of the database.
- `restore_database()`: Restores the database from a backup file.
- `main()`: The main program loop handling user input and menu navigation.

Future Enhancements

- Password Strength Checker: Evaluate the strength of user-provided passwords and suggest improvements.
- Password Update Feature: Allow users to update passwords without deleting and re-adding entries.
- Integration with Cloud Storage: Add options to backup/restore databases from cloud storage services (e.g., Google Drive).
- Multi-User Support: Enable multi-user functionality, allowing each user to have their own set of passwords.

Security Considerations

- Encryption: The password manager uses AES encryption (via `cryptography` library) to ensure that passwords are stored securely.
- Two-Factor Authentication (2FA): The application uses Time-based One-Time Passwords (TOTP) to provide an additional layer of security.
- Backup Security: Ensure that backups are stored in secure locations to prevent unauthorized access.

License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Contribution

Contributions are welcome! Feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
