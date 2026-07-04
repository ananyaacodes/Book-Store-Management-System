"""
auth.py
-------
Handles password hashing and both login systems:

- signup()/login()        -> regular buyer accounts (table: signup)
- admin_login()            -> staff/admin accounts (table: admin_credentials)

Passwords are never stored in plain text. We use PBKDF2-HMAC-SHA256
with a random salt per user (via Python's built-in hashlib, so no
extra dependency is needed).
"""

import hashlib
import hmac
import os
import binascii
import getpass

import db

PBKDF2_ITERATIONS = 200_000


def hash_password(password: str) -> str:
    """Return 'salt$hash' (both hex-encoded) for storage."""
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"{binascii.hexlify(salt).decode()}${binascii.hexlify(derived).decode()}"


def verify_password(password: str, stored: str) -> bool:
    """Check a plaintext password against a stored 'salt$hash' value."""
    try:
        salt_hex, hash_hex = stored.split("$")
    except (ValueError, AttributeError):
        return False

    salt = binascii.unhexlify(salt_hex)
    expected = binascii.unhexlify(hash_hex)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return hmac.compare_digest(derived, expected)


# ------------------------- buyer accounts -------------------------

def signup(cur, con):
    username = input("Choose a username: ").strip()

    existing = db.fetch_one(cur, "SELECT username FROM signup WHERE username=%s", (username,))
    if existing:
        print("That username is already taken.")
        return

    password = getpass.getpass("Choose a password: ")
    hashed = hash_password(password)

    db.execute(cur, con, "INSERT INTO signup (username, password) VALUES (%s, %s)",
               (username, hashed))
    print("Signup successful! You can now log in.")


def login(cur, con) -> bool:
    username = input("Username: ").strip()
    row = db.fetch_one(cur, "SELECT password FROM signup WHERE username=%s", (username,))

    if not row:
        print("User not found.")
        return False

    password = getpass.getpass("Password: ")
    if verify_password(password, row[0]):
        print("Login successful!")
        return True

    print("Incorrect password.")
    return False


# ------------------------- admin accounts -------------------------

def ensure_admin_bootstrap(cur, con):
    """If no admin account exists yet, prompt to create the first one.
    This runs once -- after that, admin_login() is used normally."""
    row = db.fetch_one(cur, "SELECT COUNT(*) FROM admin_credentials")
    if row and row[0] > 0:
        return

    print("No admin account exists yet. Let's create one.")
    username = input("New admin username: ").strip()
    password = getpass.getpass("New admin password: ")
    hashed = hash_password(password)
    db.execute(cur, con, "INSERT INTO admin_credentials (username, password) VALUES (%s, %s)",
               (username, hashed))
    print("Admin account created.")


def admin_login(cur, con) -> bool:
    username = input("Admin username: ").strip()
    row = db.fetch_one(cur, "SELECT password FROM admin_credentials WHERE username=%s", (username,))

    if not row:
        print("Admin not found.")
        return False

    password = getpass.getpass("Admin password: ")
    if verify_password(password, row[0]):
        print("Admin login successful!")
        return True

    print("Incorrect password.")
    return False