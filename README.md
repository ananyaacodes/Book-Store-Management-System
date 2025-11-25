# 📚 Book Store Management System

A complete Python + MySQL based Book Store Management System that allows staff and users to manage inventory, purchase books, search books, view staff details, track sales, and handle income reports. This project is perfect for demonstrating Python database connectivity, CRUD operations, and structured menu-driven applications.

## 🚀 Features

👨‍💼 Admin / Staff Functions

* Add new books

* Manage staff (Add / Remove / View)

* View available books

* View sales records

* Reset sales history

* View total income

* Update book quantities

👤 User Functions

* Sign up & Login

* Purchase books

* Search books by:

    * Name

   * Genre

   * Author

* View available books

* View staff details

## 🛠️Tech Stack

| Component | Technology |
|-----------|------------|
| Language  | Python 3   |
| Database  | MySQL      |
| Library   | mysql-connector-python |
| Concepts  | CRUD, SQL Queries, Functions, Loops, Validation |


## 📁 Project Structure

Book_Store_Management_System/

│

├── Library Management System.py                 # Main program file

├── requirements.txt                             # Dependencies

├── README.md                                    # Project documentation

└── .gitignore                                   # Ignored files

## 🧩Install Dependencies 

Install MySQL connector:

pip install mysql-connector-python

## 🗄️Database Setup

### 1. Create the database:

```sql
CREATE DATABASE bookstore;
```

### 2. Required tables:

```sql
CREATE TABLE available_books(
    bookname VARCHAR(100),
    genre VARCHAR(50),
    quantity INT,
    author VARCHAR(100),
    publication VARCHAR(100),
    price INT
);

CREATE TABLE staff_details(
    name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    phoneno BIGINT,
    address VARCHAR(255)
);

CREATE TABLE sell_rec(
    buyer_name VARCHAR(100),
    phone BIGINT,
    book VARCHAR(100),
    quantity INT,
    price INT
);

CREATE TABLE signup(
    username VARCHAR(50),
    password VARCHAR(50)
);
```

## ▶️Run the Program
python "Library Management System.py"

## 📌Future Improvements

* Add GUI using Tkinter

* Add password hashing

* Add admin login system

* Add invoice generation

* Add email notifications (optional)

## 📜License

This project is under the MIT License.
