"""
db.py
-----
Owns the MySQL connection and exposes small helper functions so the
rest of the codebase never has to build SQL strings by hand.

Every query here uses parameterized placeholders (%s), so user input
is always passed as data, never concatenated into the query text.
This is what prevents SQL injection.
"""

import sys
import mysql.connector
from mysql.connector import Error

import config


def get_connection():
    """Open and return a new MySQL connection, or exit with a clear
    error message if the connection fails."""
    try:
        con = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
        )
        if con.is_connected():
            print("Connected to the database successfully!")
        return con
    except Error as e:
        print(f"Could not connect to the database: {e}")
        sys.exit(1)


def ensure_schema(cur, con):
    """Create tables if they don't already exist, including the new
    admin_credentials table used by the admin login system."""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS available_books(
            bookname VARCHAR(100),
            genre VARCHAR(50),
            quantity INT,
            author VARCHAR(100),
            publication VARCHAR(100),
            price INT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS staff_details(
            name VARCHAR(100),
            gender VARCHAR(10),
            age INT,
            phoneno BIGINT,
            address VARCHAR(255)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sell_rec(
            buyer_name VARCHAR(100),
            phone BIGINT,
            book VARCHAR(100),
            quantity INT,
            price INT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS signup(
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(255)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_credentials(
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(255)
        )
    """)
    con.commit()


# ---------------------- generic query helpers ----------------------

def fetch_all(cur, query, params=()):
    cur.execute(query, params)
    return cur.fetchall()


def fetch_one(cur, query, params=()):
    cur.execute(query, params)
    return cur.fetchone()


def execute(cur, con, query, params=()):
    cur.execute(query, params)
    con.commit()