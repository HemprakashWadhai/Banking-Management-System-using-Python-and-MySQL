import mysql.connector as m
from getpass import getpass

# Connect to MySQL
connection = m.connect(
    host='localhost',
    user='root',
    password='1432'
)

cursor = connection.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS banking_system")
cursor.execute("USE banking_system")

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    account_number VARCHAR(12) PRIMARY KEY,
    name VARCHAR(255),
    mobile_number VARCHAR(10),
    adhar_card_number VARCHAR(12),
    Adress varchar(1000),
    balance DECIMAL(10, 2) DEFAULT 0.0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(255)
)
""")

# Set a password function
def set_password():
    cursor.execute("SELECT * FROM auth")
    if cursor.fetchone() is None:
        password = getpass("Create a password: ")
        cursor.execute("INSERT INTO auth (password) VALUES (%s)", (password,))
        connection.commit()
        print("Password set successfully.")
    else:
        print("Password already set.")

# Validate password
def validate_password():
    password = getpass("Enter password: ")
    cursor.execute("SELECT password FROM auth WHERE id = 1")
    stored_password = cursor.fetchone()[0]
    if password == stored_password:
        return True
    else:
        print("Invalid password.")
        return False

# Create an account
def create_account():
    account_number = (input("Enter 12-digit account number: "))
    if len(account_number) != 12:
        print("Account number must be 12 digits.")
        return print("invalid numbers please enter 12 digit numbers")
    name = input("Enter your name: ")
    mobile_number = input("Enter 10-digit  mobile number: ")
    adhar_card_number = input("Enter 12-digit Aadhar card number: ")
    Adress = input("Enter your Current Address: ")

    cursor.execute("INSERT INTO users (account_number, name, mobile_number, adhar_card_number, Adress) VALUES (%s, %s, %s, %s, %s)", 
                   (account_number, name, mobile_number, adhar_card_number, Adress))
    connection.commit()
    print("Account created successfully.")

# Check balance
def check_balance():
    if not validate_password():
        return
    account_number = input("Enter your account number: ")
    cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    if result:
        print(f"Your balance is: {result[0]}")
    else:
        print("Invalid account number.")

# Deposit money
def deposit():
    if not validate_password():
        return
    account_number = input("Enter your account number: ")
    amount = float(input("Enter amount to deposit: "))
    cursor.execute("UPDATE users SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
    connection.commit()
    cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    if result:
        print(f"Amount deposited successfully. Your new balance is: {result[0]}")
    else:
        print("Error updating balance.")

# Withdraw money
def withdraw():
    if not validate_password():
        return
    account_number = input("Enter your account number: ")
    amount = float(input("Enter amount to withdraw: "))
    cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    if result and result[0] >= amount:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
        connection.commit()
        cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_number,))
        updated_result = cursor.fetchone()
        if updated_result:
            print(f"Amount withdrawn successfully. Your new balance is: {updated_result[0]}")
        else:
            print("Error updating balance.")
    else:
        print("Insufficient balance or invalid account number.")
# Menu
def menu():
    while True:
        print("\nWelcome to the Banking System")
        print("1. Account Creation")
        print("2. Balance Check")
        print("3. Withdraw Money")
        print("4. Deposit Money")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            create_account()
        elif choice == '2':
            check_balance()
        elif choice == '3':
            withdraw()
        elif choice == '4':
            deposit()
        elif choice == '5':
            print("Thank you for using the banking system.")
            break
        else:
            print("Invalid choice. Please try again.")

# Initialize system
set_password()
menu()

# Close the connection
connection.close()
