"""
config.py
---------
Central place for configuration values.

Credentials are read from environment variables instead of being
hardcoded in source, so the repo can be safely committed to GitHub.

Set these before running the program (e.g. in a `.env` file loaded
with python-dotenv, or exported in your shell):

    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_mysql_password
    DB_NAME=bookstore
"""

import os

# Optional: load a local .env file if python-dotenv is installed.
# This is not required -- if the package isn't installed, or there's
# no .env file, we just fall back to whatever is already in the
# environment (e.g. exported in the shell, or set by the OS/CI).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME", "bookstore")

if DB_PASSWORD is None:
    raise EnvironmentError(
        "DB_PASSWORD is not set. Create a .env file (see .env.example) "
        "or export it in your shell before running the program."
    )

# Where generated invoices are saved.
INVOICE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "invoices")