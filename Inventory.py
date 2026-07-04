"""
inventory.py
------------
Everything to do with the available_books table: adding stock,
listing it, and the three search modes buyers can use.
"""

import db


def _print_book_row(row):
    bookname, genre, quantity, author, publication, price = row
    print("****************************************************")
    print("Book Name:", bookname)
    print("Genre:", genre)
    print("Available:", quantity)
    print("Author:", author)
    print("Publication:", publication)
    print("Price:", price)
    print("****************************************************")


def add_book(cur, con):
    while True:
        book = input("Enter Book Name: ").strip()
        genre = input("Genre: ").strip()

        try:
            quantity = int(input("Enter quantity: "))
            price = int(input("Enter the price: "))
        except ValueError:
            print("Quantity and price must be whole numbers. Please try again.")
            continue

        author = input("Enter author name: ").strip()
        publication = input("Enter publication house: ").strip()

        db.execute(
            cur, con,
            "INSERT INTO available_books (bookname, genre, quantity, author, publication, price) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (book, genre, quantity, author, publication, price),
        )
        print("++++++++++++++++++++++++SUCCESSFULLY ADDED++++++++++++++++++++++++")

        if input("Add another? (y/n): ").strip().lower() != "y":
            break


def view_available(cur):
    rows = db.fetch_all(cur, "SELECT * FROM available_books ORDER BY bookname")
    if not rows:
        print("No books in stock yet.")
        return
    for row in rows:
        _print_book_row(row)


def update_quantity(cur, con, bookname: str, delta: int):
    """delta is negative for a sale, positive for restocking."""
    db.execute(
        cur, con,
        "UPDATE available_books SET quantity = quantity + %s WHERE bookname = %s",
        (delta, bookname),
    )


def get_book(cur, bookname: str):
    return db.fetch_one(
        cur, "SELECT * FROM available_books WHERE bookname = %s", (bookname,)
    )


def search_by_name(cur):
    while True:
        name = input("Enter book name to search: ").strip()
        row = db.fetch_one(cur, "SELECT bookname FROM available_books WHERE bookname=%s", (name,))
        print("++++ BOOK IS IN STOCK ++++" if row else "BOOK NOT AVAILABLE")

        if input("Search again? (y/n): ").strip().lower() != "y":
            break


def search_by_genre(cur):
    while True:
        genre = input("Enter genre to search: ").strip()
        rows = db.fetch_all(cur, "SELECT * FROM available_books WHERE genre=%s", (genre,))

        if rows:
            print("++++ BOOKS AVAILABLE ++++")
            for row in rows:
                _print_book_row(row)
        else:
            print("No books found for this genre.")

        if input("Search again? (y/n): ").strip().lower() != "y":
            break


def search_by_author(cur):
    while True:
        author = input("Enter author name: ").strip()
        rows = db.fetch_all(cur, "SELECT * FROM available_books WHERE author=%s", (author,))
        print("++++ BOOKS AVAILABLE ++++" if rows else "NO BOOKS BY THIS AUTHOR")

        if input("Search again? (y/n): ").strip().lower() != "y":
            break