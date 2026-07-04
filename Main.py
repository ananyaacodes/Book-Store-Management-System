"""
main.py
-------
Entry point. Wires together db/auth/inventory/staff/sales into the
same menu structure as the original program, but with:
  - a real admin login gating the staff side
  - while-loops instead of recursive "continue?" prompts
  - graceful handling of bad input (no more crashing on int())
"""

import db
import auth
import inventory
import staff
import sales


def staff_menu(cur, con):
    while True:
        print("""
1. Add Books
2. Staff Menu
3. Sell Record
4. Total Income
5. View Available Books
6. Log out
""")
        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            inventory.add_book(cur, con)

        elif choice == "2":
            print("""
1. New Staff
2. Remove Staff
3. View Staff Details
""")
            sub = input("Enter choice: ").strip()
            if sub == "1":
                staff.add_staff(cur, con)
            elif sub == "2":
                staff.remove_staff(cur, con)
            elif sub == "3":
                staff.view_staff(cur)
            else:
                print("Invalid choice.")

        elif choice == "3":
            print("""
1. Sell History
2. Reset Sell History
""")
            sub = input("Enter choice: ").strip()
            if sub == "1":
                sales.view_sell_records(cur)
            else:
                sales.reset_sell_history(cur, con)

        elif choice == "4":
            sales.total_income(cur)

        elif choice == "5":
            inventory.view_available(cur)

        elif choice == "6":
            return

        else:
            print("Invalid choice.")


def buyer_menu(cur, con):
    while True:
        print("""
1. Purchase Books
2. Search Books
3. Available Books
4. Staff Details
5. Log out
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            sales.purchase(cur, con)

        elif choice == "2":
            print("""
1. Search by Name
2. Search by Genre
3. Search by Author
""")
            sub = input("Search by: ").strip()
            if sub == "1":
                inventory.search_by_name(cur)
            elif sub == "2":
                inventory.search_by_genre(cur)
            else:
                inventory.search_by_author(cur)

        elif choice == "3":
            inventory.view_available(cur)

        elif choice == "4":
            staff.view_staff(cur)

        elif choice == "5":
            return

        else:
            print("Invalid choice.")


def main():
    con = db.get_connection()
    cur = con.cursor()
    db.ensure_schema(cur, con)
    auth.ensure_admin_bootstrap(cur, con)

    print("*************** WELCOME TO BOOK STORE ***************")

    try:
        while True:
            print("""
1. Employee Login
2. User Login
3. Exit
""")
            choice = input("Enter: ").strip()

            if choice == "1":
                if auth.admin_login(cur, con):
                    staff_menu(cur, con)

            elif choice == "2":
                print("""
1. Signup
2. Login
""")
                sub = input("Choice: ").strip()
                if sub == "1":
                    auth.signup(cur, con)
                else:
                    if auth.login(cur, con):
                        buyer_menu(cur, con)

            elif choice == "3":
                break

            else:
                print("Invalid choice.")
    finally:
        cur.close()
        con.close()


if __name__ == "__main__":
    main()