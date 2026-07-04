"""
staff.py
--------
Staff record management (name/gender/age/phone/address). This is
separate from admin login credentials -- these are just personnel
records the admin keeps, not accounts anyone logs in with.
"""

import db


def add_staff(cur, con):
    while True:
        fname = input("Enter Fullname: ").strip()
        gender = input("Gender(M/F/O): ").strip()

        try:
            age = int(input("Age: "))
            phno = int(input("Staff phone no.: "))
        except ValueError:
            print("Age and phone number must be numbers. Please try again.")
            continue

        address = input("Address: ").strip()

        db.execute(
            cur, con,
            "INSERT INTO staff_details (name, gender, age, phoneno, address) "
            "VALUES (%s, %s, %s, %s, %s)",
            (fname, gender, age, phno, address),
        )
        print("++++++++++++ STAFF SUCCESSFULLY ADDED ++++++++++++")

        if input("Add another? (y/n): ").strip().lower() != "y":
            break


def remove_staff(cur, con):
    while True:
        name = input("Staff Name to Remove: ").strip()
        db.execute(cur, con, "DELETE FROM staff_details WHERE name=%s", (name,))
        print("Employee Removed.")

        if input("Remove another? (y/n): ").strip().lower() != "y":
            break


def view_staff(cur):
    rows = db.fetch_all(cur, "SELECT * FROM staff_details")
    if not rows:
        print("No staff on record.")
        return

    for name, gender, age, phoneno, address in rows:
        print("************************************")
        print("Name:", name)
        print("Gender:", gender)
        print("Age:", age)
        print("Phone No:", phoneno)
        print("Address:", address)
        print("************************************")