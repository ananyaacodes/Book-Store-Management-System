import mysql.connector
con = mysql.connector.connect(
    host="Localhost",
    user="root",
    password="pass_26",
    database="bookstore"
)

if con.is_connected():
    print("Connected successfully!")



if con.is_connected():
    print('yes')

cur = con.cursor()

# -------------------- ADMIN FUNCTIONS ------------------------

def ADD():
    book = input("Enter Book Name: ")
    genre = input("Genre: ")
    quantity = int(input("Enter quantity: "))
    author = input("Enter author name: ")
    publication = input("Enter publication house: ")
    price = int(input("Enter the price: "))

    cur.execute(
        "INSERT INTO available_books (bookname, genre, quantity, author, publication, price) VALUES (%s, %s, %s, %s, %s, %s)",
        (book, genre, quantity, author, publication, price)
    )
    con.commit()

    print("++++++++++++++++++++++++SUCCESSFULLY ADDED++++++++++++++++++++++++")

    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        ADD()
    else:
        Staff()


def NewStaff():
    fname = input("Enter Fullname: ")
    gender = input("Gender(M/F/O): ")
    age = int(input("Age: "))
    phno = int(input("Staff phone no.: "))
    add = input("Address: ")

    cur.execute(f"INSERT INTO staff_details VALUES('{fname}','{gender}',{age},{phno},'{add}')")
    con.commit()

    print("++++++++++++ STAFF SUCCESSFULLY ADDED ++++++++++++")
    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        NewStaff()
    else:
        Staff()


def RemoveStaff():
    n = input("Staff Name to Remove: ")
    cur.execute(f"DELETE FROM staff_details WHERE Name='{n}'")
    con.commit()

    print("Employee Removed.")
    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        RemoveStaff()
    else:
        Staff()


def StaffDetailfS():
    cur.execute("SELECT * FROM staff_details")
    output = cur.fetchall()

    for x in output:
        print("************************************")
        print("Name:", x[0])
        print("Gender:", x[1])
        print("Age:", x[2])
        print("Phone No:", x[3])
        print("Address:", x[4])
        print("************************************")

    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        StaffDetailfS()
    else:
        Staff()


def SellRec():
    cur.execute("SELECT * FROM sell_rec")

    for u in cur:
        print("*********************************************")
        print("Buyer Name:", u[0])
        print("Buyer Mobile:", u[1])
        print("Book:", u[2])
        print("Quantity:", u[3])
        print("Price:", u[4])
        print("*********************************************")

    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        SellRec()
    else:
        Staff()


def DelRec():
    bb = input("Are you sure(Y/N): ").upper()
    if bb == "Y":
        cur.execute("DELETE FROM sell_rec")
        con.commit()

    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        DelRec()
    else:
        Staff()


def TotalIncome():
    cur.execute("SELECT SUM(price) FROM sell_rec")
    for x in cur:
        print("Total Sell Till Date:", x)

    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        TotalIncome()
    else:
        Staff()


def AvailablefS():
    cur.execute("SELECT * FROM available_books ORDER BY bookname")

    for v in cur:
        print("****************************************************")
        print("Book Name:", v[0])
        print("Genre:", v[1])
        print("Available:", v[2])
        print("Author:", v[3])
        print("Publication:", v[4])
        print("Price:", v[5])
        print("****************************************************")

    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        AvailablefS()
    else:
        Staff()


# ----------------------- BUYER FUNCTIONS ------------------------

def AvailablefU():
    cur.execute("SELECT * FROM available_books ORDER BY bookname")

    for v in cur:
        print("****************************************************")
        print("Book Name:", v[0])
        print("Genre:", v[1])
        print("Available:", v[2])
        print("Author:", v[3])
        print("Publication:", v[4])
        print("Price:", v[5])
        print("****************************************************")

    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        AvailablefU()
    else:
        Buyer()


def StaffDetailfU():
    cur.execute("SELECT * FROM staff_details")
    output = cur.fetchall()

    for x in output:
        print("************************************")
        print("Name:", x[0])
        print("Gender:", x[1])
        print("Age:", x[2])
        print("Phone No:", x[3])
        print("Address:", x[4])
        print("************************************")

    n = int(input("Want To Continue:\n1. Yes\n2. No\nOPTION: "))
    if n == 1:
        StaffDetailfU()
    else:
        Buyer()


def Purchase():
    print("AVAILABLE BOOKS...")
    cur.execute("SELECT * FROM available_books")

    for i in cur:
        print("****************************************************")
        print("Book Name:", i[0])
        print("Genre:", i[1])
        print("Available:", i[2])
        print("Author:", i[3])
        print("Publication:", i[4])
        print("Price:", i[5])
        print("****************************************************")

    cusname = input("Enter customer name: ")
    phno = int(input("Enter phone number: "))
    book = input("Enter Book Name: ")
    price = int(input("Enter the price: "))
    n = int(input("Enter quantity: "))

    cur.execute(f"SELECT quantity FROM available_books WHERE bookname='{book}'")
    k = cur.fetchone()

    if k is None or k[0] < n:
        print("Books are not available!")
        Buyer()
        return

    cur.execute(f"INSERT INTO sell_rec VALUES('{cusname}','{phno}','{book}','{n}','{price}')")
    cur.execute(f"UPDATE available_books SET quantity=quantity-{n} WHERE bookname='{book}'")
    con.commit()

    print("++++++++++++ BOOK SOLD ++++++++++++")
    Buyer()


def UsingName():
    o = input("Enter Book to search: ")
    cur.execute(f"SELECT bookname FROM available_books WHERE bookname='{o}'")
    t = cur.fetchone()

    if t:
        print("++++ BOOK IS IN STOCK ++++")
    else:
        print("BOOK NOT AVAILABLE")

    n = int(input("1. Continue\n2. Exit\nOPTION: "))
    if n == 1:
        UsingName()
    else:
        Buyer()


def UsingGenre():
    g = input("Enter genre to search: ")
    cur.execute(f"SELECT * FROM available_books WHERE genre='{g}'")
    poll = cur.fetchall()

    if poll:
        print("++++ BOOKS AVAILABLE ++++")
        for y in poll:
            print("*******************************************")
            print("Book Name:", y[0])
            print("Genre:", y[1])
            print("Quantity:", y[2])
            print("Author:", y[3])
            print("Publication:", y[4])
            print("Price:", y[5])
            print("*******************************************")
    else:
        print("No books found for this genre.")

    n = int(input("1. Continue\n2. Exit\nOPTION: "))
    if n == 1:
        UsingGenre()
    else:
        Buyer()


def UsingAuthor():
    o = input("Enter author name: ")
    cur.execute(f"SELECT * FROM available_books WHERE author='{o}'")
    t = cur.fetchall()

    if t:
        print("++++ BOOKS AVAILABLE ++++")
    else:
        print("NO BOOKS BY THIS AUTHOR")

    n = int(input("1. Continue\n2. Exit\nOPTION: "))
    if n == 1:
        UsingAuthor()
    else:
        Buyer()


# ---------------------- STAFF MAIN MENU --------------------------

def Staff():
    print("""
1. Add Books
2. Staff Menu
3. Sell Record
4. Total Income
5. View Available Books
6. Exit
""")
    n = int(input("Enter Your Choice: "))

    if n == 1:
        ADD()

    elif n == 2:
        print("""
1. New Staff
2. Remove Staff
3. View Staff Details
""")
        ch = int(input("Enter choice: "))
        if ch == 1:
            NewStaff()
        elif ch == 2:
            RemoveStaff()
        elif ch == 3:
            StaffDetailfS()

    elif n == 3:
        print("""
1. Sell History
2. Reset Sell History
""")
        ty = int(input("Enter choice: "))
        if ty == 1:
            SellRec()
        else:
            DelRec()

    elif n == 4:
        TotalIncome()

    elif n == 5:
        AvailablefS()

    elif n == 6:
        return


# ---------------------- BUYER MAIN MENU --------------------------

def Buyer():
    print("""
1. Purchase Books
2. Search Books
3. Available Books
4. Staff Details
5. Exit
""")
    r = int(input("Enter your choice: "))

    if r == 1:
        Purchase()

    elif r == 2:
        print("""
1. Search by Name
2. Search by Genre
3. Search by Author
""")
        l = int(input("Search by: "))
        if l == 1:
            UsingName()
        elif l == 2:
            UsingGenre()
        else:
            UsingAuthor()

    elif r == 3:
        AvailablefU()

    elif r == 4:
        StaffDetailfU()

    elif r == 5:
        return


# ---------------------- MAIN PROGRAM --------------------------

print("*************** WELCOME TO BOOK STORE ***************")

while True:
    a = int(input("""
1. Employee Login
2. User Login
3. Exit
Enter: """))

    if a == 1:
        Staff()

    elif a == 2:
        print("""
1. Signup
2. Login
""")
        s = int(input("Choice: "))

        if s == 1:
            user_name = input("USERNAME: ")
            password = input("PASSWORD: ")
            cur.execute(f"INSERT INTO signup VALUES('{user_name}','{password}')")
            con.commit()
            print("Signup Successful!")

        else:
            user2 = input("Enter Username: ")
            cur.execute(f"SELECT username FROM signup WHERE username='{user2}'")
            b = cur.fetchone()

            if b:
                b1 = input("Enter Password: ")
                cur.execute(f"SELECT password FROM signup WHERE password='{b1}'")
                a2 = cur.fetchone()
                if a2:
                    print("Login Successful!")
                    Buyer()
                else:
                    print("Incorrect Password")

            else:
                print("User Not Found")

    elif a == 3:
        break
