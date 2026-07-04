"""
sales.py
--------
Handles purchases, the sell_rec history table, total income, and
generating a text invoice for each completed sale.
"""

import os
import datetime

import db
import inventory
import config


def _generate_invoice(cusname, phone, book, quantity, unit_price):
    """Write a simple text invoice to config.INVOICE_DIR and return its path."""
    os.makedirs(config.INVOICE_DIR, exist_ok=True)

    timestamp = datetime.datetime.now()
    total = quantity * unit_price
    filename = f"invoice_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(config.INVOICE_DIR, filename)

    lines = [
        "=============================================",
        "               BOOK STORE INVOICE             ",
        "=============================================",
        f"Date       : {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Customer   : {cusname}",
        f"Phone      : {phone}",
        "---------------------------------------------",
        f"Book       : {book}",
        f"Quantity   : {quantity}",
        f"Unit Price : {unit_price}",
        "---------------------------------------------",
        f"TOTAL      : {total}",
        "=============================================",
        "        Thank you for your purchase!          ",
        "=============================================",
    ]

    with open(filepath, "w") as f:
        f.write("\n".join(lines) + "\n")

    return filepath, lines


def purchase(cur, con):
    print("AVAILABLE BOOKS...")
    inventory.view_available(cur)

    cusname = input("Enter customer name: ").strip()

    try:
        phno = int(input("Enter phone number: "))
    except ValueError:
        print("Phone number must be numeric. Purchase cancelled.")
        return

    book = input("Enter Book Name: ").strip()
    row = inventory.get_book(cur, book)

    if row is None:
        print("That book isn't in stock.")
        return

    _, _, available_qty, _, _, unit_price = row

    try:
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Quantity must be a number. Purchase cancelled.")
        return

    if quantity <= 0 or quantity > available_qty:
        print("Books are not available in that quantity!")
        return

    db.execute(
        cur, con,
        "INSERT INTO sell_rec (buyer_name, phone, book, quantity, price) VALUES (%s, %s, %s, %s, %s)",
        (cusname, phno, book, quantity, unit_price),
    )
    inventory.update_quantity(cur, con, book, -quantity)

    print("++++++++++++ BOOK SOLD ++++++++++++")

    filepath, lines = _generate_invoice(cusname, phno, book, quantity, unit_price)
    print("\n".join(lines))
    print(f"\nInvoice saved to: {filepath}")


def view_sell_records(cur):
    rows = db.fetch_all(cur, "SELECT * FROM sell_rec")
    if not rows:
        print("No sales recorded yet.")
        return

    for buyer_name, phone, book, quantity, price in rows:
        print("*********************************************")
        print("Buyer Name:", buyer_name)
        print("Buyer Mobile:", phone)
        print("Book:", book)
        print("Quantity:", quantity)
        print("Price:", price)
        print("*********************************************")


def reset_sell_history(cur, con):
    confirm = input("Are you sure you want to clear all sale history? (Y/N): ").strip().upper()
    if confirm == "Y":
        db.execute(cur, con, "DELETE FROM sell_rec")
        print("Sell history cleared.")
    else:
        print("Cancelled.")


def total_income(cur):
    row = db.fetch_one(cur, "SELECT SUM(price * quantity) FROM sell_rec")
    total = row[0] if row and row[0] is not None else 0
    print("Total Sales Till Date:", total)